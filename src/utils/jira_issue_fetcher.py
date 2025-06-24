 import requests
import os
from typing import List, Dict, Optional

class JiraIssueFetcher:
    def __init__(self, base_url: str, api_token: str, username: str, project_key: str, output_dir: str = './jira_output'):
        """
        初始化Jira工单抓取器
        :param base_url: Jira实例URL
        :param api_token: API Token
        :param username: 用户名
        :param project_key: 项目Key
        :param output_dir: 输出目录
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.username = username
        self.project_key = project_key
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.auth = (self.username, self.api_token)
        self.session.headers.update({'Accept': 'application/json'})
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_issues(self, jql: str = None) -> List[Dict]:
        """
        批量获取Jira工单（可通过JQL筛选）
        :param jql: JQL查询语句，如 'project=XXX'
        :return: 工单列表
        """
        pass

    def fetch_issue_detail(self, issue_id_or_key: str) -> Dict:
        """
        获取单个工单的详细信息
        :param issue_id_or_key: 工单ID或Key
        :return: 工单详情字典
        """
        pass

    def fetch_issue_comments(self, issue_id_or_key: str) -> List[Dict]:
        """
        获取工单的所有评论
        :param issue_id_or_key: 工单ID或Key
        :return: 评论列表
        """
        pass

    def fetch_issue_attachments(self, issue_id_or_key: str) -> List[Dict]:
        """
        获取工单的所有附件元信息
        :param issue_id_or_key: 工单ID或Key
        :return: 附件元信息列表
        """
        pass

    def download_attachments(self, attachments: List[Dict]):
        """
        下载附件到本地output目录
        :param attachments: 附件元信息列表
        """
        pass

    def save_issue_as_md(self, issue: Dict, comments: List[Dict] = None):
        """
        保存工单为Markdown文件（可带评论）
        :param issue: 工单详情
        :param comments: 评论列表
        """
        pass

    def save_issue_as_json(self, issue: Dict):
        """
        保存工单为JSON文件
        :param issue: 工单详情
        """
        pass

    def run(self, jql: str = None):
        """
        主流程：批量抓取工单并保存
        :param jql: JQL查询语句
        """
        pass

    def fetch_projects(self) -> List[Dict]:
        """
        获取所有项目列表
        :return: 项目列表
        """
        pass

    def fetch_users(self, query: str = None) -> List[Dict]:
        """
        查询用户（可用于分配工单）
        :param query: 用户名或邮箱模糊查询
        :return: 用户列表
        """
        pass
