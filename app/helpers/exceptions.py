class SSPException(BaseException):
    def __init__(self):
        self.message = (
            "The SSP Toolkit files are missing. The SSP Toolkit files should "
            "live in a directory in this project root directory named `ssp`."
        )
        super().__init__(self.message)
