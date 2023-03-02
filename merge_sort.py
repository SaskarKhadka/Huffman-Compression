def merge_sort(arr):
    '''
    Sorts the given array by using Merge Sort algorithm 
    '''

    # array contains Node elements
    if len(arr) > 1:

        #  Divide array into 2 parts at mid_point
        mid_point = len(arr) // 2
        left = arr[:mid_point]
        right = arr[mid_point:]

        # Recusively divide
        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        # Conquer
        # sort and add elements of left and right to original array
        while i < len(left) and j < len(right):
            if left[i].freq < right[j].freq:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # Add remaining elements in arr
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
