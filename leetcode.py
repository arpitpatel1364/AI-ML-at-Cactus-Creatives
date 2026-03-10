# class Solution:
#     def twoSum(self, nums, target: int):
#         for i in nums:
#             for j in nums:
#                 if i + j == target :
#                     print (i,j)
#                     A= nums.index(i)
#                     B=nums.index(j)
#                     L1=[]
#                     L1.append(A)
#                     L1.append(B)
#                     print(L1)    
#                     return L1
#                 else :              
#                   continue
#             break

# solution=Solution()
# print(solution.twoSum([2, 7, 11, 15],13)) 
class Solution:
    def twoSum(self, nums, target: int):
        for i in nums:
            for j in nums:
                if i + j == target :
                    print (i,j)
                    A= nums.index(i)
                    B=nums.index(j)
                    L1=[]
                    L1.append(A)
                    L1.append(B)
                    print(L1)    
                    return L1
                else :              
                  continue
            break

solution=Solution()
while True:
    user=input("add list:")
    I3=(input("enter your number :"))
    I1=[]
    I1.append(I3)
    break

I2=input ("enter target value")

print(solution.twoSum(I1,I2)) 