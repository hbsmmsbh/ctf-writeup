**Challenge**: web/scrainbow
Oh no! someone dropped my perfect gradient and it shattered into 10000 pieces! I can't figure out how to put it back together anymore, it never looks quite right. Can you help me fix it? URL: http://litctf.org:31780/

------------

**Analysis**:
This problem is not difficult in itself, but it looks complicated. Because it is a 100*100 dot matrix, you need to find an automatic algorithm to find the answer.

**Step 1**: After several attempts, you will find：
1. The dot matirx data could be obtained via "http://litctf.org:31780/data" get request.
1. The final solution data could be sent via "http://litctf.org:31780/test" post request.

**Step 2**: Our target: Rearrange the grid to be a rainbow gradient from top left to bottom right (red -> rainbow -> red)
With the help of ChatGPT, we can find an automatic algorithm as below:
1. Convert hex colors to HSL and sort by Hue
1. Rearrange sorted colors diagonally into a 100x100 grid
1. Prepare the solution data:
- Compare the original grid & final grid.
- If same, then keep it,
- If not, then find the first occurrence of color value after the current position, then swap them.
------------

**Final Solution**:
Please find the python solution file: [scrainbow_solution.py](https://github.com/hbsmmsbh/ctf-writeup/blob/main/Lexington%20Informatics%20Tournament%20CTF/2024/web/scrainbow_solution.py "scrainbow_solution.py")
