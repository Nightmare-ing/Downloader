import unittest
from google_drive_downloader import download_docs_with_id, download_file_with_id, get_file_id, create_service
from download import setup_logging

class TestGoogleDownloadsLocal(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.creds, self.service = create_service()
        self.storage_path = "outputs"
        setup_logging()

    def test_presentation_without_edit(self):
        link = "https://docs.google.com/presentation/d/1hRUkaONWvWP7IZbINLP-G6uOyyulDqury5kop7638co"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["pptx", "pdf"])
        
    def test_presentation_with_edit(self):
        link =  "https://docs.google.com/presentation/d/1ADK25v7v3HaATJETk5W9NSWvRA_Y18WDLsgkphWHzCI/edit?usp=share_link"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["pptx", "pdf"])
    
    def test_drive_file(self):
        link = "https://drive.google.com/file/d/10TBXmYiDwyN4hIBEctfuRYDqyZyotDOn/view?usp=sharing"
        file_id = get_file_id(link)
        download_file_with_id(self.storage_path, file_id, self.creds, "pdf")
    
    def test_drive_file_with_open(self):
        link = "https://drive.google.com/open?id=1DjliLLJrZVlN_GcFcIVgEzTfLKpaeZQ8"
        file_id = get_file_id(link)
        download_file_with_id(self.storage_path, file_id, self.creds, "mp4")
            
    def test_docs_without_edit(self):
        link = "https://docs.google.com/document/d/1JqfsZrSlf63v__sRdMjeFUMOXpklDAWcVeQx-EOVyDo"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["docx", "pdf"])

    def test_docs_with_edit(self):
        link = "https://docs.google.com/document/d/1JqfsZrSlf63v__sRdMjeFUMOXpklDAWcVeQx-EOVyDo/edit?usp=sharing"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["docx", "pdf"])
    

class TestGoogleDownloadsProxy(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.creds, self.service = create_service()
        self.storage_path = "outputs"
        setup_logging()

    def test_presentation_without_edit(self):
        link = "https://docs.google.com/presentation/d/1ELBsq-eVk7NzsDu_FubqYsp9qytiYaA8UXt0dc9X57c"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["pptx", "pdf"])
        
    def test_presentation_with_edit(self):
        link = "https://docs.google.com/presentation/d/1k3zZWMQtFtwXV8vGpgnUCEIr63WTqwDi/edit"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["pptx", "pdf"])
    
    def test_drive_file(self):
        link = "https://drive.google.com/file/d/1CsjoMtea8XskYthAFmi5LeHPPmQuOOiK/view?usp=sharing"
        file_id = get_file_id(link)
        download_file_with_id(self.storage_path, file_id, self.creds, "pdf")
    
    def test_drive_file_with_open(self):
        link = "https://drive.google.com/open?id=1-cnBUgx9AkH-mwG1m0H5hFGSgG8gwZbO"
        file_id = get_file_id(link)
        download_file_with_id(self.storage_path, file_id, self.creds, "mp4")
            
    def test_docs_with_edit(self):
        link = "https://docs.google.com/document/d/1oVXrDPgkPZdaAuH_spkYRJKgVN7QAFXlopm9q7L9GMc/edit?usp=sharing"
        file_id = get_file_id(link)
        download_docs_with_id(self.storage_path, file_id, self.service, types=["docx", "pdf"])

if __name__ == "__main__":
    unittest.main()