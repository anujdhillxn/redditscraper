class trieNode:
    def __init__(self):
        self.bit = {}
        self.ends = ''

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
            st[-1].bit[data[i]] = p
            if(data[i+1] == '+'):
                p.ends = data[i+1]
                i += 2
            else:
                i+= 1

    return root

#root = trieNode()
#f_final = open("posted.csv", "r")

#for line in f_final:
#    insert(root, line.split(',')[0])

#f = open("serialized_database.txt",'a')
#f.write(serialize(root))
#f.close()