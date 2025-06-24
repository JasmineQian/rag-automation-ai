import requests
import os
import yaml
from markdownify import markdownify as md
from typing import List, Dict, Optional
import re


class ConfluencePageFetcher:
    def __init__(self, base_url: str, api_token: str, username: str, space_key: str, output_dir: str = './output'):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.username = username
        self.space_key = space_key
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.auth = (self.username, self.api_token)
        self.session.headers.update({'Accept': 'application/json'})
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_all_pages(self) -> List[Dict]:
        """
        递归获取空间下所有页面的元信息（id, title, parent_id, author, created, updated, url）
        """
        all_pages = []
        start = 0
        limit = 50
        while True:
            url = f"{self.base_url}/rest/api/content?spaceKey={self.space_key}&limit={limit}&start={start}&expand=ancestors,version,history"
            resp = self.session.get(url)
            resp.raise_for_status()
            data = resp.json()
            for page in data.get('results', []):
                meta = {
                    'id': page['id'],
                    'title': page['title'],
                    'parent_id': page['ancestors'][-1]['id'] if page.get('ancestors') else None,
                    'author': page['history']['createdBy']['displayName'] if 'history' in page and 'createdBy' in page[
                        'history'] else '',
                    'created': page['history']['createdDate'] if 'history' in page else '',
                    'updated': page['version']['when'] if 'version' in page else '',
                    'url': f"{self.base_url}/pages/viewpage.action?pageId={page['id']}"
                }
                all_pages.append(meta)
            if data['_links'].get('next'):
                start += limit
            else:
                break
        return all_pages

    def fetch_page_content(self, page_id: str) -> str:
        """
        获取单个页面的 HTML 内容
        """
        url = f"{self.base_url}/rest/api/content/{page_id}?expand=body.storage"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data['body']['storage']['value']

    def save_page_as_md(self, page: Dict, content: str):
        """
        保存页面为 Markdown 文件，带 YAML frontmatter
        """
        meta = {
            'title': page['title'],
            'id': page['id'],
            'parent_id': page.get('parent_id'),
            'author': page.get('author'),
            'created': page.get('created'),
            'updated': page.get('updated'),
            'url': page.get('url')
        }
        md_content = f"---\n{yaml.dump(meta, allow_unicode=True)}---\n\n{content}"
        safe_title = page['title'].replace('/', '_').replace('\\', '_')
        filename = f"{page['id']}-{safe_title}.md"
        with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(md_content)

    def run(self):
        """
        主流程：批量抓取所有页面并保存为 Markdown
        """
        pages = self.fetch_all_pages()
        for page in pages:
            try:
                html_content = self.fetch_page_content(page['id'])
                md_content = md(html_content)
                self.save_page_as_md(page, md_content)
                print(f"已保存: {page['title']}")
            except Exception as e:
                print(f"抓取或保存页面 {page['title']} 失败: {e}")

    def fetch_spaces(self) -> list:
        """
        获取所有空间的 key 和名称，便于查找正确的 spaceKey
        """
        url = f"{self.base_url}/rest/api/space?limit=100"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        spaces = []
        for space in data.get('results', []):
            info = {
                'key': space.get('key'),
                'name': space.get('name'),
                'type': space.get('type', ''),
                'id': space.get('id', '')
            }
            spaces.append(info)
            print(f"key: {info['key']}, name: {info['name']}, type: {info['type']}")
        return spaces

    def fetch_and_save_by_url(self, url: str):
        """
        通过页面URL抓取并保存该页面内容到output文件夹
        :param url: 形如 https://xxx/wiki/pages/viewpage.action?pageId=123456
        """
        match = re.search(r'pageId=(\d+)', url)
        if not match:
            print(f"无法从URL中提取pageId: {url}")
            return
        page_id = match.group(1)
        try:
            html_content = self.fetch_page_content(page_id)
            md_content = md(html_content)
            # 获取页面元信息
            page_meta_url = f"{self.base_url}/rest/api/content/{page_id}?expand=ancestors,version,history"
            resp = self.session.get(page_meta_url)
            resp.raise_for_status()
            data = resp.json()
            page = {
                'id': data['id'],
                'title': data['title'],
                'parent_id': data['ancestors'][-1]['id'] if data.get('ancestors') else None,
                'author': data['history']['createdBy']['displayName'] if 'history' in data and 'createdBy' in data['history'] else '',
                'created': data['history']['createdDate'] if 'history' in data else '',
                'updated': data['version']['when'] if 'version' in data else '',
                'url': url
            }
            self.save_page_as_md(page, md_content)
            print(f"已保存: {page['title']}")
        except Exception as e:
            print(f"抓取或保存页面失败: {e}")


if __name__ == '__main__':
    # 从环境变量中获取Jira URL和Token
    from dotenv import load_dotenv
    load_dotenv()  # 自动加载 .env 文件
    jira_url = os.getenv('JIRA_URL', 'https://liveramp.atlassian.net/wiki/')  # 替换为你的Jira实例URL
    jira_token = os.getenv('JIRA_TOKEN')
    username = os.getenv('JIRA_NAME', 'your_username')  # 替换为你的Jira用户名
    space_key= os.getenv('SPACE_KEY', '~600f010665f20b0070a81ea0')  # 替换为你的Confluence空间键
    jira_instance = ConfluencePageFetcher(jira_url, jira_token, username,space_key)  # 替换为你的Jira实例URL
    # 示例：通过url抓取并保存单个页面
    # page_url = 'https://your-domain/wiki/pages/viewpage.action?pageId=123456'
    # jira_instance.fetch_and_save_by_url(page_url)
    # jira_instance.run()
    
    page_id=4849827841
    # pages = jira_instance.fetch_all_pages()  # 获取指定空间下的所有页面
    # for page in pages:
    #     if page['id'] ==page_id:
    #         print(f"找到页面: {page['title']} (ID: {page['id']})")
    #         page_dict = jira_instance.fetch_page_content(page_id)  # 获取单个页面内容
    #         md_content = md(page_dict)
    #         jira_instance.save_page_as_md(page, md_content) # 保存为Markdown文件
    jira_instance.fetch_and_save_by_url(f'https://liveramp.atlassian.net/wiki/pages/viewpage.action?pageId={page_id}')