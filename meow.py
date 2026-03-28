import os
import struct
import shutil

def littleNum(v: int, length: int) -> bytes:
    return v.to_bytes(length, "little", signed=False)

def getFileName(path: str) -> str:
    return os.path.split(path)[1]

class MEOW:
    def __init__(self) -> None:
        self.files = []

    def addFile(self, path: str) -> None:
        if os.path.exists(path):
            self.files.append(path)
        else:
            print(f"{path} does not exist :c")

    def removeFiles(self) -> None:
        self.files.clear()

    def combineFiles(self, fileName: str) -> None:
        fileName += ".meow"
        with open(fileName, "wb") as fileOut:
            fileOut.write(b"Meow")
            fileOut.write(littleNum(0x1ba5, 2))

            for file in self.files:
                with open(file, "rb") as fileData:
                    name = getFileName(file)
                    length = os.path.getsize(file)

                    # 1 byte:  file name length
                    # x bytes: file name
                    # 8 bytes: file size
                    # y bytes: file content

                    fileOut.write(littleNum(len(name) & 0xff, 1))
                    fileOut.write(name.encode("utf-8"))

                    fileOut.write(littleNum(length, 8))
                    fileOut.write(fileData.read())

            fileOut.write(littleNum(0x00, 1))

    def separateFiles(self, path: str) -> None:
        with open(path, "rb") as fileIn:
            marker, magicNumber = struct.unpack("<4sH", fileIn.read(6))
            if not ((marker == b"Meow") and (magicNumber == 0x1ba5)):
                print(f"{path} is not a .meow file >:3c")
                return

            outPath = f"{os.path.splitext(getFileName(path))[0]}/"
            if os.path.exists(outPath):
                shutil.rmtree(outPath)
            os.makedirs(outPath)

            while 1:
                fileNameLen = struct.unpack("<B", fileIn.read(1))[0]
                if fileNameLen == 0x00:
                    break
                fileName, fileLen = struct.unpack(f"<{fileNameLen}sQ", fileIn.read(fileNameLen + 8))
                fileName = fileName.decode("utf-8")
                with open(outPath + fileName, "xb") as fileOut:
                    fileOut.write(fileIn.read(fileLen))
