import urllib2
import sys
import copy

TARGET = 'http://crypto-class.appspot.com/po?er='
CT = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding


def decrypt(ct, po):
    pt_list = []

    pt_list.insert(0, crack_first_block(3, ct, po))

    for i in range(0, len(ct) - 2):
        ct_index = len(ct) - 2 - i
        pt_list.insert(0, crack_block(ct_index, ct, po))

    plaintext = ''
    for i in range(0, len(pt_list)):
        plaintext = plaintext + ''.join(pt_list[i])

    print plaintext

def crack_block(block_to_crack_index, ct, po):
    test_ct = copy.deepcopy(ct)
    pt = []

    for l in range(0, len(ct) - block_to_crack_index - 2):
        test_ct.pop()

    for i in range(0, 16):
        update_prev_padding(pt, ct, test_ct, i, block_to_crack_index)

        #Iterate through the guesses
        for j in range(0, 256):
            if (try_guess(ct, test_ct, i, j, po, block_to_crack_index)) == True:
                print 'DECRYPTYED CHAR: \'' + chr(j) + '\''
                pt.insert(0, chr(j))
                break

    return pt

def crack_first_block(block_to_crack_index, ct, po):
    orig_padded_val = -1
    test_ct = copy.deepcopy(ct)
    pt = []

    for j in range(0, 256):
        if (try_guess(ct, test_ct, 0, j, po, block_to_crack_index)) == True:
            orig_padded_val = j
            break

    for i in range(0, orig_padded_val):
        pt.insert(0, ' ')

    for i in range(orig_padded_val, 16):

        padding_val = i + 1
        # Update the original padding
        for k in range(0, orig_padded_val):
            ct_char = ct[block_to_crack_index - 1][15 - k]
            test_val = ord(ct_char) ^ orig_padded_val ^ padding_val
            test_ct[block_to_crack_index - 1][15 - k] = chr(test_val)

        # Update the padding
        for k in range(orig_padded_val, i):
            guessed_char = pt[len(pt) - 1 - k]
            ct_char = ct[block_to_crack_index - 1][15 - k]
            test_val = ord(ct_char) ^ ord(guessed_char) ^ padding_val
            test_ct[block_to_crack_index - 1][15 - k] = chr(test_val)

        #Iterate through the guesses
        for j in range(0, 256):
            if (try_guess(ct, test_ct, i, j, po, block_to_crack_index)) == True:
                print 'DECRYPTYED CHAR: \'' + chr(j) + '\''
                pt.insert(0, chr(j))
                break

    return pt

def update_prev_padding(pt, ct, test_ct, i, block_to_crack_index):
    padding_val = i + 1

    for k in range(0, i):
        guessed_char = pt[len(pt) - 1 - k]
        ct_char = ct[block_to_crack_index - 1][15 - k]
        test_val = ord(ct_char) ^ ord(guessed_char) ^ padding_val
        test_ct[block_to_crack_index - 1][15 - k] = chr(test_val)

def try_guess(ct, test_ct, i, guess, po, block_to_crack_index):
    ct_char = ct[block_to_crack_index - 1][15 - i]
    padding_val = (i + 1)

    test_val = ord(ct_char) ^ guess ^ padding_val
    test_ct[block_to_crack_index - 1][15 - i] = chr(test_val)

    return po.query(get_test_str(block_to_crack_index, test_ct))

def get_test_str(block_to_crack_index, test_ct):
    test_str = ''
    for m in range(0, block_to_crack_index + 1):
        test_str = test_str + ''.join(test_ct[m])
    test_str = test_str.encode('Hex')

    return test_str

def combine_blocks_into_string(ct):
    test_str = (''.join(ct[0]) + ''.join(ct[1]) + ''.join(ct[2]))
    return test_str.encode('Hex')

def break_into_blocks():
    temp = CT.decode('hex')
    ct = []
    for i in range(0, (len(temp) / 16)):
        temp_arr = list(temp[i * 16 : (i + 1) * 16])
        ct.insert(i, temp_arr)

    return ct

if __name__ == "__main__":
    po = PaddingOracle()
    ct = break_into_blocks()
    decrypt(ct, po)
