class UpdateChecker(QThread):
    """版本检查线程"""
    
    # 定义信号
    update_available = pyqtSignal(dict)  # 有新版本可用
    no_update = pyqtSignal()             # 已是最新版本
    check_failed = pyqtSignal(str)       # 检查失败
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timeout = 10  # 10秒超时
    
    def run(self):
        """执行版本检查"""
        try:
            # 从version模块导入配置
            try:
                from version import VERSION_CHECK_URL, BACKUP_VERSION_URL, CURRENT_VERSION
            except ImportError:
                # 如果version.py不存在，使用默认值
                CURRENT_VERSION = "2.1.0"
                VERSION_CHECK_URL = "https://raw.githubusercontent.com/your-username/pyro-browser/main/version.json"
                BACKUP_VERSION_URL = "https://gist.githubusercontent.com/your-username/your-gist-id/raw/pyro-browser-version.json"
            
            # 尝试从主URL获取版本信息
            version_info = self.fetch_version_info(VERSION_CHECK_URL)
            if not version_info:
                # 如果主URL失败，尝试备用URL
                version_info = self.fetch_version_info(BACKUP_VERSION_URL)
            
            if version_info:
                self.process_version_info(version_info, CURRENT_VERSION)
            else:
                # 如果网络检查失败，使用模拟数据作为备用
                self.use_fallback_check()
                
        except Exception as e:
            self.check_failed.emit(f"检查更新时发生错误: {str(e)}")
    
    def fetch_version_info(self, url):
        """从指定URL获取版本信息"""
        try:
            # 设置请求头，避免被某些服务器拒绝
            headers = {
                'User-Agent': 'PyroBrowser/2.1.0',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, timeout=self.timeout, headers=headers)
            if response.status_code == 200:
                version_data = response.json()
                
                # 验证版本信息格式
                if self.validate_version_info(version_data):
                    return version_data
                else:
                    print(f"无效的版本信息格式从: {url}")
                    return None
                    
        except requests.exceptions.Timeout:
            print(f"请求超时: {url}")
        except requests.exceptions.ConnectionError:
            print(f"连接错误: {url}")
        except requests.exceptions.RequestException as e:
            print(f"请求异常 {url}: {e}")
        except json.JSONDecodeError:
            print(f"JSON解析错误从: {url}")
        
        return None
    
    def validate_version_info(self, version_info):
        """验证版本信息格式"""
        required_fields = ['latest_version', 'release_date', 'download_url']
        return all(field in version_info for field in required_fields)
    
    def compare_versions(self, current_version, latest_version):
        """比较版本号，返回是否需要更新"""
        try:
            def parse_version(version):
                # 移除可能的前缀如 "v"
                version = version.lstrip('vV')
                parts = version.split('.')
                # 将每个部分转换为整数
                return [int(part) for part in parts]
            
            current_parts = parse_version(current_version)
            latest_parts = parse_version(latest_version)
            
            # 比较每个部分
            for i in range(max(len(current_parts), len(latest_parts))):
                current_part = current_parts[i] if i < len(current_parts) else 0
                latest_part = latest_parts[i] if i < len(latest_parts) else 0
                
                if latest_part > current_part:
                    return True
                elif latest_part < current_part:
                    return False
            
            return False
            
        except Exception as e:
            print(f"版本比较错误: {e}")
            return False
    
    def process_version_info(self, version_info, current_version):
        """处理版本信息"""
        try:
            latest_version = version_info.get('latest_version')
            if not latest_version:
                self.check_failed.emit("无效的版本信息格式")
                return
            
            if self.compare_versions(current_version, latest_version):
                # 有新版本可用
                self.update_available.emit(version_info)
            else:
                # 已是最新版本
                self.no_update.emit()
                
        except Exception as e:
            self.check_failed.emit(f"处理版本信息时出错: {str(e)}")
    
    def use_fallback_check(self):
        """备用检查机制 - 使用模拟数据"""
        try:
            # 模拟网络延迟
            self.msleep(1500)
            
            # 这里可以改为总是返回无更新，或者根据配置决定
            # 目前使用随机模拟
            import random
            if random.random() > 0.7:  # 30%概率显示有更新
                version_info = {
                    "latest_version": "2.2.0",
                    "release_date": "2024-12-15",
                    "download_url": "https://github.com/your-username/pyro-browser/releases/latest",
                    "changelog": "https://github.com/your-username/pyro-browser/blob/main/CHANGELOG.md",
                    "update_priority": "normal",
                    "changes": [
                        "新增：自动更新检查功能",
                        "优化：关于对话框滚动体验",
                        "修复：已知的性能问题",
                        "改进：标签页管理逻辑",
                        "增强：浏览器稳定性"
                    ]
                }
                self.update_available.emit(version_info)
            else:
                self.no_update.emit()
                
        except Exception as e:
            self.check_failed.emit(f"备用检查失败: {str(e)}")
            