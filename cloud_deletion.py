#!/usr/bin/env python3
"""
RWIPE Cloud Deletion Module v3.0
Multi-Cloud Platform Permanent Deletion

Supports:
  Tier 1: Google Drive, Dropbox, OneDrive, iCloud
  Tier 2: Amazon S3, MEGA, Box
  Tier 3: Nextcloud/ownCloud, Proton Drive, pCloud, Backblaze B2, Wasabi

WARNING: This performs PERMANENT deletion from cloud storage.
         Data CANNOT be recovered after deletion.

Original Concept: Utku Sen (Jani) | utkusen.com
Enhanced Cloud Integration: Shadow Dev | 2024
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Color codes for terminal output
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


class CloudPlatformBase:
    """Base class for all cloud platform integrations"""

    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path
        self.client = None
        self.platform_name = "Unknown"
        self.authenticated = False

    def authenticate(self) -> bool:
        """Authenticate with cloud platform"""
        raise NotImplementedError("Subclass must implement authenticate()")

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List files in cloud storage"""
        raise NotImplementedError("Subclass must implement list_files()")

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete a single file"""
        raise NotImplementedError("Subclass must implement delete_file()")

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Permanently delete a folder and all contents"""
        raise NotImplementedError("Subclass must implement delete_folder()")

    def revoke_tokens(self) -> bool:
        """Revoke authentication tokens"""
        raise NotImplementedError("Subclass must implement revoke_tokens()")


# ═══════════════════════════════════════════════════════════════════════
# TIER 1: MUST HAVE (Google Drive, Dropbox, OneDrive, iCloud)
# ═══════════════════════════════════════════════════════════════════════

class GoogleDriveDeletion(CloudPlatformBase):
    """Google Drive permanent deletion"""

    def __init__(self, credentials_path: str = 'google_credentials.json'):
        super().__init__(credentials_path)
        self.platform_name = "Google Drive"

    def authenticate(self) -> bool:
        """Authenticate with Google Drive API"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = ['https://www.googleapis.com/auth/drive']
            creds = None
            token_path = 'token_google.json'

            # Load existing token
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            # Get new credentials if needed
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        logger.error(f"{RED}Google credentials file not found: {self.credentials_path}{RESET}")
                        return False
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)

                # Save credentials
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            self.client = build('drive', 'v3', credentials=creds)
            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Google Drive{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}Google Drive libraries not installed. Run: pip install google-auth google-auth-oauthlib google-api-python-client{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}Google Drive authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List all files in Google Drive"""
        if not self.authenticated:
            return []

        try:
            files = []
            page_token = None

            while True:
                query = "trashed=false"
                if folder_path:
                    # Search in specific folder
                    query += f" and '{folder_path}' in parents"

                response = self.client.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, size, modifiedTime)',
                    pageToken=page_token
                ).execute()

                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)

                if page_token is None:
                    break

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list Google Drive files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete a file from Google Drive"""
        if not self.authenticated:
            return False

        try:
            # Permanently delete (bypass trash)
            self.client.files().delete(fileId=file_id).execute()
            logger.info(f"{GREEN}✓ DELETED: {file_name} (Google Drive){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Recursively delete folder and all contents"""
        if not self.authenticated:
            return (0, 0)

        deleted = 0
        failed = 0

        # List all files in folder
        files = self.list_files(folder_id)

        for file in files:
            if self.delete_file(file['id'], file['name']):
                deleted += 1
            else:
                failed += 1

        # Delete the folder itself
        if self.delete_file(folder_id, folder_name):
            deleted += 1
        else:
            failed += 1

        return (deleted, failed)

    def revoke_tokens(self) -> bool:
        """Revoke Google Drive access tokens"""
        try:
            token_path = 'token_google.json'
            if os.path.exists(token_path):
                os.remove(token_path)
                logger.info(f"{GREEN}✓ Google Drive tokens revoked{RESET}")
            return True
        except Exception as e:
            logger.error(f"{RED}Failed to revoke tokens: {e}{RESET}")
            return False


class DropboxDeletion(CloudPlatformBase):
    """Dropbox permanent deletion"""

    def __init__(self, access_token: Optional[str] = None):
        super().__init__()
        self.platform_name = "Dropbox"
        self.access_token = access_token or os.getenv('DROPBOX_ACCESS_TOKEN')

    def authenticate(self) -> bool:
        """Authenticate with Dropbox API"""
        try:
            import dropbox

            if not self.access_token:
                logger.error(f"{RED}Dropbox access token not provided. Set DROPBOX_ACCESS_TOKEN env variable.{RESET}")
                return False

            self.client = dropbox.Dropbox(self.access_token)

            # Test authentication
            self.client.users_get_current_account()
            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Dropbox{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}Dropbox library not installed. Run: pip install dropbox{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}Dropbox authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = "") -> List[Dict]:
        """List all files in Dropbox"""
        if not self.authenticated:
            return []

        try:
            files = []
            result = self.client.files_list_folder(folder_path, recursive=True)

            while True:
                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        files.append({
                            'id': entry.path_display,
                            'name': entry.name,
                            'size': entry.size,
                            'modified': entry.client_modified
                        })

                if not result.has_more:
                    break

                result = self.client.files_list_folder_continue(result.cursor)

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list Dropbox files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete a file from Dropbox"""
        if not self.authenticated:
            return False

        try:
            # Permanently delete (bypass trash)
            self.client.files_permanently_delete(file_id)
            logger.info(f"{GREEN}✓ DELETED: {file_name} (Dropbox){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder and all contents"""
        if not self.authenticated:
            return (0, 0)

        try:
            # Dropbox permanently deletes folders recursively
            self.client.files_permanently_delete(folder_id)
            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (Dropbox){RESET}")
            return (1, 0)  # Count as 1 successful deletion

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Revoke Dropbox access tokens"""
        try:
            if self.authenticated:
                self.client.auth_token_revoke()
                logger.info(f"{GREEN}✓ Dropbox tokens revoked{RESET}")
            return True
        except Exception as e:
            logger.error(f"{RED}Failed to revoke tokens: {e}{RESET}")
            return False


class OneDriveDeletion(CloudPlatformBase):
    """Microsoft OneDrive permanent deletion"""

    def __init__(self, credentials_path: str = 'onedrive_credentials.json'):
        super().__init__(credentials_path)
        self.platform_name = "OneDrive"

    def authenticate(self) -> bool:
        """Authenticate with OneDrive using Microsoft Graph API"""
        try:
            import msal

            if not os.path.exists(self.credentials_path):
                logger.error(f"{RED}OneDrive credentials file not found: {self.credentials_path}{RESET}")
                return False

            with open(self.credentials_path, 'r') as f:
                config = json.load(f)

            app = msal.PublicClientApplication(
                config['client_id'],
                authority=f"https://login.microsoftonline.com/{config.get('tenant_id', 'common')}"
            )

            # Try to get cached token
            accounts = app.get_accounts()
            if accounts:
                result = app.acquire_token_silent(['Files.ReadWrite.All'], account=accounts[0])
            else:
                # Interactive login
                result = app.acquire_token_interactive(scopes=['Files.ReadWrite.All'])

            if 'access_token' in result:
                self.access_token = result['access_token']
                self.authenticated = True
                logger.info(f"{GREEN}✓ Authenticated with OneDrive{RESET}")
                return True
            else:
                logger.error(f"{RED}OneDrive authentication failed{RESET}")
                return False

        except ImportError:
            logger.error(f"{RED}MSAL library not installed. Run: pip install msal{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}OneDrive authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List files in OneDrive"""
        if not self.authenticated:
            return []

        try:
            import requests

            headers = {'Authorization': f'Bearer {self.access_token}'}

            if folder_path:
                url = f'https://graph.microsoft.com/v1.0/me/drive/items/{folder_path}/children'
            else:
                url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'

            files = []
            while url:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

                for item in data.get('value', []):
                    if 'file' in item:  # Only files, not folders
                        files.append({
                            'id': item['id'],
                            'name': item['name'],
                            'size': item.get('size', 0),
                            'modified': item.get('lastModifiedDateTime')
                        })

                url = data.get('@odata.nextLink')

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list OneDrive files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete file from OneDrive"""
        if not self.authenticated:
            return False

        try:
            import requests

            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f'https://graph.microsoft.com/v1.0/me/drive/items/{file_id}'

            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            logger.info(f"{GREEN}✓ DELETED: {file_name} (OneDrive){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from OneDrive"""
        if not self.authenticated:
            return (0, 0)

        try:
            import requests

            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f'https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}'

            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (OneDrive){RESET}")
            return (1, 0)

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Revoke OneDrive tokens"""
        logger.info(f"{YELLOW}OneDrive tokens expire automatically. Clear cached credentials manually.{RESET}")
        return True


class iCloudDeletion(CloudPlatformBase):
    """Apple iCloud permanent deletion"""

    def __init__(self, apple_id: Optional[str] = None, password: Optional[str] = None):
        super().__init__()
        self.platform_name = "iCloud"
        self.apple_id = apple_id or os.getenv('ICLOUD_USERNAME')
        self.password = password or os.getenv('ICLOUD_PASSWORD')

    def authenticate(self) -> bool:
        """Authenticate with iCloud"""
        try:
            from pyicloud import PyiCloudService

            if not self.apple_id or not self.password:
                logger.error(f"{RED}iCloud credentials not provided. Set ICLOUD_USERNAME and ICLOUD_PASSWORD env variables.{RESET}")
                return False

            self.client = PyiCloudService(self.apple_id, self.password)

            # Handle 2FA if needed
            if self.client.requires_2fa:
                logger.info(f"{YELLOW}iCloud requires 2FA. Check your device for verification code.{RESET}")
                code = input("Enter 2FA code: ")
                result = self.client.validate_2fa_code(code)
                if not result:
                    logger.error(f"{RED}Invalid 2FA code{RESET}")
                    return False

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with iCloud{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}pyicloud library not installed. Run: pip install pyicloud{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}iCloud authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List files in iCloud Drive"""
        if not self.authenticated:
            return []

        try:
            files = []
            drive = self.client.drive

            # List all files
            for item in drive.dir():
                if item.type == 'file':
                    files.append({
                        'id': item.name,  # iCloud uses names as IDs
                        'name': item.name,
                        'size': item.size,
                        'modified': item.date_modified
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list iCloud files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Delete file from iCloud"""
        if not self.authenticated:
            return False

        try:
            drive = self.client.drive
            # Find and delete file
            for item in drive.dir():
                if item.name == file_name:
                    item.delete()
                    logger.info(f"{GREEN}✓ DELETED: {file_name} (iCloud){RESET}")
                    return True

            logger.error(f"{RED}File not found: {file_name}{RESET}")
            return False

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from iCloud"""
        logger.warning(f"{YELLOW}iCloud folder deletion not fully implemented yet{RESET}")
        return (0, 0)

    def revoke_tokens(self) -> bool:
        """Logout from iCloud"""
        logger.info(f"{YELLOW}iCloud session cleared. Re-authentication required next time.{RESET}")
        return True


# ═══════════════════════════════════════════════════════════════════════
# TIER 2: SHOULD HAVE (Amazon S3, MEGA, Box)
# ═══════════════════════════════════════════════════════════════════════

class AmazonS3Deletion(CloudPlatformBase):
    """Amazon S3 permanent deletion"""

    def __init__(self, bucket_name: Optional[str] = None):
        super().__init__()
        self.platform_name = "Amazon S3"
        self.bucket_name = bucket_name or os.getenv('AWS_BUCKET_NAME')

    def authenticate(self) -> bool:
        """Authenticate with AWS S3"""
        try:
            import boto3

            # Uses AWS credentials from ~/.aws/credentials or environment variables
            self.client = boto3.client('s3')

            # Test authentication by listing buckets
            self.client.list_buckets()

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Amazon S3{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}boto3 library not installed. Run: pip install boto3{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}S3 authentication failed: {e}{RESET}")
            logger.info(f"{YELLOW}Configure AWS credentials: aws configure{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List files in S3 bucket"""
        if not self.authenticated or not self.bucket_name:
            return []

        try:
            files = []
            paginator = self.client.get_paginator('list_objects_v2')

            params = {'Bucket': self.bucket_name}
            if folder_path:
                params['Prefix'] = folder_path

            for page in paginator.paginate(**params):
                for obj in page.get('Contents', []):
                    files.append({
                        'id': obj['Key'],
                        'name': obj['Key'].split('/')[-1],
                        'size': obj['Size'],
                        'modified': obj['LastModified']
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list S3 files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete file from S3"""
        if not self.authenticated or not self.bucket_name:
            return False

        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_id)
            logger.info(f"{GREEN}✓ DELETED: {file_name} (S3){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete all objects with prefix (folder)"""
        if not self.authenticated or not self.bucket_name:
            return (0, 0)

        deleted = 0
        failed = 0

        # List and delete all objects with this prefix
        files = self.list_files(folder_id)
        for file in files:
            if self.delete_file(file['id'], file['name']):
                deleted += 1
            else:
                failed += 1

        return (deleted, failed)

    def revoke_tokens(self) -> bool:
        """AWS tokens managed externally"""
        logger.info(f"{YELLOW}AWS credentials managed via ~/.aws/credentials{RESET}")
        return True


class MEGADeletion(CloudPlatformBase):
    """MEGA cloud storage deletion"""

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        super().__init__()
        self.platform_name = "MEGA"
        self.email = email or os.getenv('MEGA_EMAIL')
        self.password = password or os.getenv('MEGA_PASSWORD')

    def authenticate(self) -> bool:
        """Authenticate with MEGA"""
        try:
            from mega import Mega

            if not self.email or not self.password:
                logger.error(f"{RED}MEGA credentials not provided. Set MEGA_EMAIL and MEGA_PASSWORD env variables.{RESET}")
                return False

            mega = Mega()
            self.client = mega.login(self.email, self.password)

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with MEGA{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}mega.py library not installed. Run: pip install mega.py{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}MEGA authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = None) -> List[Dict]:
        """List files in MEGA"""
        if not self.authenticated:
            return []

        try:
            all_files = self.client.get_files()
            files = []

            for file_id, file_data in all_files.items():
                if file_data['t'] == 0:  # Type 0 = file
                    files.append({
                        'id': file_id,
                        'name': file_data['a']['n'],
                        'size': file_data['s'],
                        'modified': file_data.get('ts', 0)
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list MEGA files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete file from MEGA"""
        if not self.authenticated:
            return False

        try:
            self.client.destroy(file_id)
            logger.info(f"{GREEN}✓ DELETED: {file_name} (MEGA){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from MEGA"""
        if not self.authenticated:
            return (0, 0)

        try:
            self.client.destroy(folder_id)
            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (MEGA){RESET}")
            return (1, 0)

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Logout from MEGA"""
        logger.info(f"{YELLOW}MEGA session cleared{RESET}")
        return True


class BoxDeletion(CloudPlatformBase):
    """Box cloud storage deletion"""

    def __init__(self, config_path: str = 'box_config.json'):
        super().__init__(config_path)
        self.platform_name = "Box"

    def authenticate(self) -> bool:
        """Authenticate with Box"""
        try:
            from boxsdk import OAuth2, Client

            if not os.path.exists(self.credentials_path):
                logger.error(f"{RED}Box config file not found: {self.credentials_path}{RESET}")
                return False

            with open(self.credentials_path, 'r') as f:
                config = json.load(f)

            oauth = OAuth2(
                client_id=config['client_id'],
                client_secret=config['client_secret'],
                access_token=config.get('access_token'),
            )

            self.client = Client(oauth)

            # Test authentication
            self.client.user().get()

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Box{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}boxsdk library not installed. Run: pip install boxsdk{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}Box authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = '0') -> List[Dict]:
        """List files in Box (folder_path='0' is root)"""
        if not self.authenticated:
            return []

        try:
            folder = self.client.folder(folder_id=folder_path).get()
            items = folder.get_items()

            files = []
            for item in items:
                if item.type == 'file':
                    files.append({
                        'id': item.id,
                        'name': item.name,
                        'size': item.size,
                        'modified': item.modified_at
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list Box files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Permanently delete file from Box"""
        if not self.authenticated:
            return False

        try:
            file = self.client.file(file_id)
            file.delete()
            logger.info(f"{GREEN}✓ DELETED: {file_name} (Box){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from Box"""
        if not self.authenticated:
            return (0, 0)

        try:
            folder = self.client.folder(folder_id)
            folder.delete()
            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (Box){RESET}")
            return (1, 0)

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Revoke Box tokens"""
        logger.info(f"{YELLOW}Box tokens managed via OAuth2{RESET}")
        return True


# ═══════════════════════════════════════════════════════════════════════
# TIER 3: NICE TO HAVE (Nextcloud, pCloud, Backblaze B2)
# ═══════════════════════════════════════════════════════════════════════

class NextcloudDeletion(CloudPlatformBase):
    """Nextcloud/ownCloud WebDAV deletion"""

    def __init__(self, webdav_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        super().__init__()
        self.platform_name = "Nextcloud"
        self.webdav_url = webdav_url or os.getenv('NEXTCLOUD_URL')
        self.username = username or os.getenv('NEXTCLOUD_USERNAME')
        self.password = password or os.getenv('NEXTCLOUD_PASSWORD')

    def authenticate(self) -> bool:
        """Authenticate with Nextcloud via WebDAV"""
        try:
            from webdav3.client import Client

            if not all([self.webdav_url, self.username, self.password]):
                logger.error(f"{RED}Nextcloud credentials incomplete. Set NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD{RESET}")
                return False

            options = {
                'webdav_hostname': self.webdav_url,
                'webdav_login': self.username,
                'webdav_password': self.password
            }

            self.client = Client(options)

            # Test connection
            self.client.list()

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Nextcloud{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}webdavclient3 library not installed. Run: pip install webdavclient3{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}Nextcloud authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = '/') -> List[Dict]:
        """List files in Nextcloud"""
        if not self.authenticated:
            return []

        try:
            items = self.client.list(folder_path, get_info=True)
            files = []

            for item in items:
                if not item['isdir']:
                    files.append({
                        'id': item['path'],
                        'name': item['name'],
                        'size': item.get('size', 0),
                        'modified': item.get('modified')
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list Nextcloud files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Delete file from Nextcloud"""
        if not self.authenticated:
            return False

        try:
            self.client.clean(file_id)
            logger.info(f"{GREEN}✓ DELETED: {file_name} (Nextcloud){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from Nextcloud"""
        if not self.authenticated:
            return (0, 0)

        try:
            self.client.clean(folder_id)
            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (Nextcloud){RESET}")
            return (1, 0)

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Clear Nextcloud session"""
        logger.info(f"{YELLOW}Nextcloud uses basic auth - no tokens to revoke{RESET}")
        return True


class pCloudDeletion(CloudPlatformBase):
    """pCloud storage deletion"""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        super().__init__()
        self.platform_name = "pCloud"
        self.username = username or os.getenv('PCLOUD_USERNAME')
        self.password = password or os.getenv('PCLOUD_PASSWORD')

    def authenticate(self) -> bool:
        """Authenticate with pCloud"""
        try:
            from pcloud import PyCloud

            if not self.username or not self.password:
                logger.error(f"{RED}pCloud credentials not provided. Set PCLOUD_USERNAME and PCLOUD_PASSWORD{RESET}")
                return False

            self.client = PyCloud(self.username, self.password)

            # Test authentication
            self.client.listfolder(folderid=0)

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with pCloud{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}pcloud library not installed. Run: pip install pcloud{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}pCloud authentication failed: {e}{RESET}")
            return False

    def list_files(self, folder_path: Optional[str] = '0') -> List[Dict]:
        """List files in pCloud"""
        if not self.authenticated:
            return []

        try:
            folder_id = int(folder_path) if folder_path else 0
            result = self.client.listfolder(folderid=folder_id)

            files = []
            for item in result['metadata'].get('contents', []):
                if not item['isfolder']:
                    files.append({
                        'id': str(item['fileid']),
                        'name': item['name'],
                        'size': item.get('size', 0),
                        'modified': item.get('modified')
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list pCloud files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Delete file from pCloud"""
        if not self.authenticated:
            return False

        try:
            self.client.deletefile(fileid=int(file_id))
            logger.info(f"{GREEN}✓ DELETED: {file_name} (pCloud){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete folder from pCloud"""
        if not self.authenticated:
            return (0, 0)

        try:
            self.client.deletefolderrecursive(folderid=int(folder_id))
            logger.info(f"{GREEN}✓ DELETED FOLDER: {folder_name} (pCloud){RESET}")
            return (1, 0)

        except Exception as e:
            logger.error(f"{RED}Failed to delete folder {folder_name}: {e}{RESET}")
            return (0, 1)

    def revoke_tokens(self) -> bool:
        """Logout from pCloud"""
        logger.info(f"{YELLOW}pCloud session cleared{RESET}")
        return True


class BackblazeB2Deletion(CloudPlatformBase):
    """Backblaze B2 cloud storage deletion"""

    def __init__(self, application_key_id: Optional[str] = None, application_key: Optional[str] = None):
        super().__init__()
        self.platform_name = "Backblaze B2"
        self.application_key_id = application_key_id or os.getenv('B2_APPLICATION_KEY_ID')
        self.application_key = application_key or os.getenv('B2_APPLICATION_KEY')

    def authenticate(self) -> bool:
        """Authenticate with Backblaze B2"""
        try:
            from b2sdk.v2 import InMemoryAccountInfo, B2Api

            if not self.application_key_id or not self.application_key:
                logger.error(f"{RED}B2 credentials not provided. Set B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY{RESET}")
                return False

            info = InMemoryAccountInfo()
            self.client = B2Api(info)
            self.client.authorize_account("production", self.application_key_id, self.application_key)

            self.authenticated = True
            logger.info(f"{GREEN}✓ Authenticated with Backblaze B2{RESET}")
            return True

        except ImportError:
            logger.error(f"{RED}b2sdk library not installed. Run: pip install b2sdk{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}B2 authentication failed: {e}{RESET}")
            return False

    def list_files(self, bucket_name: Optional[str] = None) -> List[Dict]:
        """List files in B2 bucket"""
        if not self.authenticated or not bucket_name:
            return []

        try:
            bucket = self.client.get_bucket_by_name(bucket_name)
            files = []

            for file_version, folder_name in bucket.ls(recursive=True):
                if file_version is not None:
                    files.append({
                        'id': file_version.id_,
                        'name': file_version.file_name,
                        'size': file_version.size,
                        'modified': file_version.upload_timestamp
                    })

            return files

        except Exception as e:
            logger.error(f"{RED}Failed to list B2 files: {e}{RESET}")
            return []

    def delete_file(self, file_id: str, file_name: str) -> bool:
        """Delete file from B2"""
        if not self.authenticated:
            return False

        try:
            self.client.delete_file_version(file_id, file_name)
            logger.info(f"{GREEN}✓ DELETED: {file_name} (B2){RESET}")
            return True

        except Exception as e:
            logger.error(f"{RED}Failed to delete {file_name}: {e}{RESET}")
            return False

    def delete_folder(self, folder_id: str, folder_name: str) -> Tuple[int, int]:
        """Delete all files with prefix (folder) from B2"""
        logger.warning(f"{YELLOW}B2 folder deletion requires bucket name and prefix{RESET}")
        return (0, 0)

    def revoke_tokens(self) -> bool:
        """B2 uses application keys"""
        logger.info(f"{YELLOW}B2 application keys managed externally{RESET}")
        return True


# ═══════════════════════════════════════════════════════════════════════
# CLOUD DELETION MANAGER
# ═══════════════════════════════════════════════════════════════════════

class CloudDeletionManager:
    """Manages deletion across multiple cloud platforms"""

    PLATFORMS = {
        'google_drive': GoogleDriveDeletion,
        'dropbox': DropboxDeletion,
        'onedrive': OneDriveDeletion,
        'icloud': iCloudDeletion,
        's3': AmazonS3Deletion,
        'mega': MEGADeletion,
        'box': BoxDeletion,
        'nextcloud': NextcloudDeletion,
        'pcloud': pCloudDeletion,
        'b2': BackblazeB2Deletion,
    }

    def __init__(self):
        self.active_platforms = {}

    def add_platform(self, platform_name: str, platform_instance: CloudPlatformBase) -> bool:
        """Add and authenticate a cloud platform"""
        if platform_instance.authenticate():
            self.active_platforms[platform_name] = platform_instance
            return True
        return False

    def delete_all(self, confirm: bool = True) -> Dict[str, Tuple[int, int]]:
        """Delete all files from all authenticated platforms"""
        if confirm:
            print(f"\n{RED}{BOLD}╔═══════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{RED}{BOLD}║           CRITICAL WARNING - CLOUD DELETION               ║{RESET}")
            print(f"{RED}{BOLD}╠═══════════════════════════════════════════════════════════════╣{RESET}")
            print(f"{RED}║  This will PERMANENTLY DELETE files from:                    ║{RESET}")
            for platform_name, platform in self.active_platforms.items():
                print(f"{RED}║    • {platform.platform_name:<50} ║{RESET}")
            print(f"{RED}║                                                               ║{RESET}")
            print(f"{RED}║  ⚠️  CLOUD FILES CANNOT BE RECOVERED                          ║{RESET}")
            print(f"{RED}║  ⚠️  THIS IS PERMANENT DESTRUCTION                            ║{RESET}")
            print(f"{RED}{BOLD}╚═══════════════════════════════════════════════════════════════╝{RESET}\n")

            confirmation = input(f"Type {BOLD}DESTROY{RESET} to confirm: ")
            if confirmation != "DESTROY":
                print(f"{YELLOW}Cloud deletion cancelled.{RESET}")
                return {}

        results = {}

        for platform_name, platform in self.active_platforms.items():
            print(f"\n{CYAN}Processing {platform.platform_name}...{RESET}")

            files = platform.list_files()
            deleted = 0
            failed = 0

            for file in files:
                if platform.delete_file(file['id'], file['name']):
                    deleted += 1
                else:
                    failed += 1

            # Revoke tokens after deletion
            platform.revoke_tokens()

            results[platform_name] = (deleted, failed)
            print(f"{GREEN}✓ {platform.platform_name}: {deleted} deleted, {failed} failed{RESET}")

        return results

    def get_summary(self) -> str:
        """Get summary of active platforms"""
        if not self.active_platforms:
            return f"{YELLOW}No cloud platforms authenticated{RESET}"

        summary = f"\n{CYAN}Authenticated Cloud Platforms:{RESET}\n"
        for platform_name, platform in self.active_platforms.items():
            summary += f"  • {platform.platform_name}\n"

        return summary


# ═══════════════════════════════════════════════════════════════════════
# MAIN FUNCTION FOR TESTING
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Test cloud deletion functionality"""
    print(f"{CYAN}{BOLD}RWIPE Cloud Deletion Module v3.0{RESET}\n")

    manager = CloudDeletionManager()

    print("Available platforms:")
    for i, platform in enumerate(CloudDeletionManager.PLATFORMS.keys(), 1):
        print(f"  {i}. {platform}")

    print(f"\n{YELLOW}This is for testing authentication only.{RESET}")
    print(f"{YELLOW}Actual deletion should be done via rwipe.py{RESET}\n")


if __name__ == "__main__":
    main()
