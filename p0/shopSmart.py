# shopSmart.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""
import shop
def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """ 
    # work done by Froylan Valencia
    # lambda expression to get shop where order value is the minimum
    # for using the cost of the order as the key value that lamda will be comparing
    # and will return the shop object associated with that key value
    return min((sh for sh in fruitShops), key=lambda sh:sh.getPriceOfOrder(orderList))
'''
for additional grading purposes I have also solved iteratively in case of uncertanty
    curr = float('inf')
    shp = None
    for s in fruitShops:
       temp = s.getPriceOfOrder(orderList) 
       if s.getPriceOfOrder(orderList)
       if temp < curr:
           curr = temp
           shp = s
     return shp
'''
if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName()
