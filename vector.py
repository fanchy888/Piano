import math
import operator
class Vector2(tuple):

	__slot__=['x','y']
	def __new__(cls,x,y=None):
		return super().__new__(cls,(x,y))
		
	def __init__(self,x,y=None):
		if y==None:
			self.x=x[0]
			self.y=x[1]
		else:
			self.x=x
			self.y=y

	def __str__(self):
		return "(%s,%s)"%(self.x,self.y)
	
	def __getitem__(self,key):
		if key==0:
			return self.x
		elif key==1:
			return self.y
		else:
			raise IndexError("Invalid subscript: "+str(key))
			
	def __setitem__(self,key,value):
		if key==1:
			self.y=value
		elif key==0:
			self.x=value 
		else:
			raise IndexError("Invalid subscript: "+str(key))
	
	def __add__(self,other):
		if (hasattr(other,'__getitem__')):
			return Vector2(other[0]+self.x,other[1]+self.y)
		else:
			return Vector2(other+self.x,other+self.y)
	__radd__=__add__
	
	def __sub__(self,other):
		if (hasattr(other,'__getitem__')):
			return Vector2(self.x-other[0],self.y-other[1])
		else:
			return Vector2(self.x-other,self.y-other)
			
	def __rsub__(self,other):
		if (hasattr(other,'__getitem__')):
			return Vector2(other[0]-self.x,other[1]-self.y)
		else:
			return Vector2(other-self.x,other-self.y)
	
	def __mul__(self,other):
		if (hasattr(other,'__getitem__')):
			return self.x*other[0]+self.y*other[1]
		else:
			return Vector2(self.x*other,self.y*other)
	__rmul__=__mul__

	def __truediv__(self, other):
		return Vector2(self.x/other,self.y/other)
		
	def __len__(self):
		return 2
		
	def __eq__(self, other):
		if hasattr(other,'__getitem__') and len(other)==2:
			return self.x==other[0] and self.y==other[1]
		else:
			return False
			
	def __ne__(self, other):
		if hasattr(other,'__getitem__') and len(other)==2:
			return self.x!=other[0] or self.y!=other[1]
		else:
			return True			
	
	def unit(self):	
		mag=self.get_mag()
		if mag!=0:
			self.x/=mag
			self.y/=mag
			
		
	def	get_mag(self):
		l=math.sqrt(self.x**2+self.y**2)
		return l
		
	@classmethod
	def from_points(cls, p1,p2):
		return cls(p2[0]-p1[0],p2[1]-p1[1])

		
if __name__=='__main__'	:	
	a=(1,2)
	b=(2.2,3.2)
	o=(-1,0)
	
	ab=Vector2.from_points(a,b)
	c=Vector2.from_points(ab,o)
	print(ab.get_mag())
	d=Vector2(c)
	e=Vector2(a)
	f=Vector2(1,2)
	g=Vector2(f)
	h=f+g
	i=Vector2(h)
	k=h
	print(k==d)
	k=a
	print(k==a)