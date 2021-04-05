class trieNode:
    def __init__(self):
        self.bit = {}
        self.ends = '-'

def insert(head,s):
    cur = head
    for b in s:
        if(b not in cur.bit):
            cur.bit[b] = trieNode()
        cur = cur.bit[b]
    cur.ends = '+'

def serialize(root):
    if(not root):
        return ""
    result = ""
    for c in root.bit:
        result += c + root.bit[c].ends + serialize(root.bit[c])
    return '<'+result+'>'

def find(head,s):
    cur = head
    for b in s:
        if(b not in cur.bit):
            return False
        cur = cur.bit[b]
    return cur.ends=='+'

def deserialize(data):
    root = trieNode()
    p = root
    st = []
    ends = ""
    i = 0
    while(i<len(data)):
        if(data[i] == '<'):
            st.append(p)
            i += 1
        elif(data[i] == '>'):
            st.pop()
            i += 1
        else:
            p = trieNode()
            p.ends = data[i+1]
            st[-1].bit[data[i]] = p
            i += 2
    return root
