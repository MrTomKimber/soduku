import numpy as np
from math import factorial, sqrt

class soduku:
    vals={0,1,2,3,4,5,6,7,8,9}
    def __init__(self, grid=None, n=3):
        self.n = n
        if grid is None:
            self.grid=np.zeros((n**2,n**2))
        else:
            self.grid=np.copy(grid)

    def copy(self):
        print ()
        return soduku(grid=self.grid, n=self.n)

    #  ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╪
    # ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋
    # ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓
    #└ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨
    #┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻
    # ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏
    # ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬
    def __str__(self):
        title =    """     ⌀   1   2   3   4   5   6   7   8   \n"""
        top =      """   ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗ \n"""
        row =      """{}  ║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║ \n"""
        mid_row =  """   ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢ \n"""
        mid_b_row ="""   ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣ \n"""
        bottom =   """   ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝ \n"""

        compiled =  title + top + \
                    row.format("⌀", *self.grid[0].astype(int)) + \
                    mid_row + \
                    row.format(1, *self.grid[1].astype(int)) + \
                    mid_row + \
                    row.format(2, *self.grid[2].astype(int)) + \
                    mid_b_row +\
                    row.format(3, *self.grid[3].astype(int)) + \
                    mid_row + \
                    row.format(4, *self.grid[4].astype(int)) + \
                    mid_row + \
                    row.format(5, *self.grid[5].astype(int)) + \
                    mid_b_row +\
                    row.format(6, *self.grid[6].astype(int)) + \
                    mid_row + \
                    row.format(7, *self.grid[7].astype(int)) + \
                    mid_row + \
                    row.format(8, *self.grid[8].astype(int)) + \
                    bottom

        return compiled.replace("0"," ").replace("⌀","0")

    def index_to_subgrid(self, index):
        return (index[0]//self.n, index[1]//self.n)

    def row_tuples(self, r):
        tups=[]
        for c in range(0,self.n**2):
            tups.append((r,c))
        return tups

    def col_tuples(self, c):
        tups=[]
        for r in range(0,self.n**2):
            tups.append((r,c))
        return tups

    def subgrid_tuples(self, sg):
        tups = []
        for r in range (0,self.n):
            for c in range(0,self.n):
                tups.append((r+(sg[0]*self.n),c+(sg[1]*self.n)))
        return tups

    def value_dict(self):
        val_dict = {}
        for v in self.vals:
            val_dict[v]=[]
            for r in range(0,self.n**2):
                for c in range(0,self.n**2):
                    if self.grid[r,c]==v:
                        val_dict[v].append((r,c))
        return val_dict

    def values(self, indices):
        return self.grid[tuple(zip(*indices))].reshape((3,3))

    def fill(self, r, c, z):
        self.grid[r][c]=z

    def fillrow(self, r, content):
        self.grid[r]=content

    def getrow(self, r, unique=False):
        if not unique:
            return self.grid[r].astype(int)
        else:
            return set(self.grid[r].astype(int))

    def getcol(self, c, unique=False):
        if not unique:
            return self.grid[:,c].astype(int)
        else:
            return set(self.grid[:,c].astype(int))

    def getreg(self, region, unique=False):
        if not unique:
            return self.grid[tuple(zip(*self.subgrid_tuples(region)))].reshape(self.n,self.n)
        else:
            return set(self.grid[tuple(zip(*self.subgrid_tuples(region)))].astype(int))

    def candidate_values(self, loc):
        r,c = loc
        a=self.getcol(c,unique=True) # values in column
        b=self.getrow(r,unique=True) # values in row
        c=self.getreg(self.index_to_subgrid(loc),unique=True) # values in region
        notin = a.union(b.union(c)) # all 1st order values that can't be in this location
        return self.vals-notin

    # Given a "group" of (r,c) indices, where the group is bound by the constraint that
    # it must contain no duplicates, and each value in vals, return a dictionary of possible gap-fills
    def get_group_candidates(self, test_group):
        gaps=[i for k,v in self.value_dict().items() for i in v if i in test_group and k==0]
        # Query to get the list of candidate fill-values for subgrid
        fills = self.vals-{k for k,v in self.value_dict().items() for i in v if i in test_group}
        #print (gaps, fills)
        # Narrow down the possible candidate gaps, by interrogating them for each fill - if an interrogation yields only
        # a single gap after filtering, then that's a match
        f_cands={}
        for f in fills:
            f_cands[f]=[]
            for g in gaps:
                #print (f, g, [v for v in s.candidate_values(g) if v==f])
                hits = [v for v in self.candidate_values(g) if v==f]
                if len(hits)>0:
                    f_cands[f].append((*g,f))
        return f_cands

    def fill_known(self, speculate=None):
        backup = self.grid.copy()
        if speculate is not None:
            self.fill(*speculate)
        finished=False
        fillers=[]
        l_count=0
        while not finished:
            l_count+=1
            c_count=0


            # This block pulls sub-grid based facts - and filters non-candidates, the same thing could apply to rows and
            # columns that have been largely filled-in.
            for g in [self.subgrid_tuples((0,0)),self.subgrid_tuples((0,1)),self.subgrid_tuples((0,2)),
                      self.subgrid_tuples((1,0)),self.subgrid_tuples((1,1)),self.subgrid_tuples((1,2)),
                      self.subgrid_tuples((2,0)),self.subgrid_tuples((2,1)),self.subgrid_tuples((2,2)),
                      self.row_tuples(0), self.row_tuples(1), self.row_tuples(2), self.row_tuples(3),
                     self.row_tuples(4), self.row_tuples(5), self.row_tuples(6), self.row_tuples(7),
                     self.row_tuples(8),self.col_tuples(0), self.col_tuples(1), self.col_tuples(2),
                      self.col_tuples(3), self.col_tuples(4), self.col_tuples(5), self.col_tuples(6),
                      self.col_tuples(7), self.col_tuples(8) ]:
                # Query to get unsolved 'gaps' in a chosen region
                f_cands = self.get_group_candidates(g)
                fu=[v[0] for k,v in f_cands.items() if len(v)==1]
                if len(fu)>0:
                    fillers.append(fu)
                    for f in [v[0] for k,v in f_cands.items() if len(v)==1]:
                        #print (f)
                        self.fill(*f)
                        c_count+=1


            for r in range(0,9):
                for c in range(0,9):
                    if int(self.grid[r][c])==0:
                        cands = self.candidate_values((r,c))
                        #print ((r,c), cands)
                        if len(cands)==1:
                            fillers.append((r,c, *cands))
                            self.fill(r,c, *cands)
                            c_count+=1
                        elif len(cands)==0: # There's been a messup somewhere - bail
                            print ("Error")
                            print (r,c, cands)
                            self.grid = backup
                            if speculate is not None:
                                print ( "{s}={v} is not a valid value".format(s=(speculate[0], speculate[1]), v=speculate[2]))
                            raise Exception("An empty square has no candidate fills.")
            if c_count==0:
                finished=True
        return fillers
