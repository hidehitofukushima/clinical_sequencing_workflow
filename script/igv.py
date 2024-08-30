import sys
import subprocess
import os



cmd = "igv"
sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out_msg, err_msg = sp.communicate()

exit_code = sp.wait()

if exit_code != 0:
    print(f"Error: Process exited with non-zero status code {exit_code}")

if out_msg:
    print("Standard Output:")
    print(out_msg.decode())

if err_msg:
    print("Standard Error:")
    print(err_msg.decode())




import unittest
import subprocess

class TestIgv(unittest.TestCase):
    def test_igv_process(self):
        cmd = "igv"
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out_msg, err_msg = sp.communicate()

        exit_code = sp.wait()

        self.assertEqual(exit_code, 0, f"Process exited with non-zero status code {exit_code}")

        if out_msg:
            self.assertTrue(True, "Standard Output:")
            self.assertTrue(True, out_msg.decode())

        if err_msg:
            self.assertTrue(True, "Standard Error:")
            self.assertTrue(True, err_msg.decode())

if __name__ == '__main__':
    unittest.main()