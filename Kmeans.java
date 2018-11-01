import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.*;
import java.util.Collections;
import java.util.HashMap;

class Element{
	double x,y;

	public Element(double x, double y) {
		super();
		this.x = x;
		this.y = y;
	}
	
}
class Data{
	double x;

	public Data(double x) {
		super();
		this.x = x;
	}
	
}
class Cluster1D{
	double xc;
	static int s=1;
	List<Data>cdata;
	 public Cluster1D() {
		// TODO Auto-generated constructor stub

		cdata=new ArrayList<>();
	             }
	 public boolean computecentre()
		{
			double xm=0;
			for(int i=0;i<cdata.size();i++)
			{
				xm=xm+cdata.get(i).x;
				
			}
			xm=xm/cdata.size();
			
			if(Math.abs(xm-xc)>0.1)
			{
				xc=xm;
			
				return true;
				
			}
			else return false;
		}
	 public void insert(Data data)
		{
			cdata.add(data);
		}
		public void remove(Data data)
		{
			cdata.remove(data);
		}
		public void print()
		{
			System.out.println("Cluster:"+s);
			s++;
			System.out.println("Center = "+xc);
			System.out.println("DataPoints :"+cdata.size());
			for(Data p:cdata)
			{
				System.out.println("Value : "+p.x);
			}
		}
	 
}
class Cluster{
	double xc,yc;
	static int s=1;
	
	List<Element>celements;
	public Cluster() {
	celements=new ArrayList<>();
             }
	public boolean computecentre()
	{
		double xm=0,ym=0;
		for(int i=0;i<celements.size();i++)
		{
			xm=xm+celements.get(i).x;
			ym=ym+celements.get(i).y;
		}
		xm=xm/celements.size();
		ym=ym/celements.size();
		if(Math.abs(xm-xc)>1||Math.abs(ym-yc)>1)
		{
			xc=xm;
			yc=ym;
			return true;
			
		}
		else return false;
	}
	public void insert(Element element)
	{
		celements.add(element);
	}
	public void remove(Element element)
	{
		celements.remove(element);
	}
	public void print()
	{
		System.out.println("Cluster:"+s);
		s++;
		System.out.println("Attribute1 center = "+xc+"\nAttribute2 center = "+yc);
		System.out.println("DataPoints :"+celements.size());
		for(Element p:celements)
		{
			System.out.println("Attr1:"+p.x+"\t\t\tAttr2:"+p.y);
		}
	}
}
public class Kmeans {
	static ArrayList<Element>elements=new ArrayList<>();
	static ArrayList<Data>data=new ArrayList<>();
	static ArrayList<Double>dist;
	static ArrayList<Double>dist1;
	static HashMap<Cluster, Integer>Map=new HashMap<>();
	static HashMap<Cluster1D, Integer>Map1=new HashMap<>();
	public static void main(String args[]) throws IOException
	{
	
	 BufferedReader br=new BufferedReader(new FileReader("C:\\Users\\Admin\\Desktop\\initialDataset.csv"));
	 String line="";
	 int f=0;
	 while((line=br.readLine())!=null)
	 { 
		 if(f==0)
		 {
			f=1;
			continue;
		 }
		 line=line.trim();
		 String d[]=line.split(",");
         Element e=new Element(Double.parseDouble(d[2]), Double.parseDouble(d[3]));
         Data dt=new Data(Double.parseDouble(d[2]));
         elements.add(e);
         data.add(dt);
         
	 }
	 
	 int nc;
	 System.out.println("Enter number of clusters");
	 
	 Scanner sc=new Scanner(System.in);
	 nc=sc.nextInt();
	 
	 Cluster c[]=new Cluster[nc];
	 Cluster1D c1[]=new Cluster1D[nc];
	 for(int i=0;i<nc;i++)
	 {
	 c[i]=new Cluster();
	 c1[i]=new Cluster1D();
	 int t=5*i;
	 c[i].xc=elements.get(i).x;
	 c[i].yc=elements.get(i).y;
	 c1[i].xc=data.get(i).x;
	 Map.put(c[i], 1);
	 Map1.put(c1[i], 1);
	 }
	
	 double d1,d2;
	 boolean a=true,b=true;

	 while(!Map1.containsValue(0))
	 {
			
		 for(Data d:data)
		 {
			 dist1 = new ArrayList<>();
		 for(int i=0;i<nc;i++)
		 {
		 dist1.add(Math.abs(c1[i].xc-d.x));
		 }
		 int mn=dist1.indexOf(Collections.min(dist1));
		    if(!c1[mn].cdata.contains(d))
			 c1[mn].insert(d);
			int k=0;
			for(k=0;k<nc;k++)
			 { if(k==mn)
				 continue;
				c1[k].remove(d);
			 }

		 }
		 for(int i=0;i<nc;i++)
		 {
			 a=c1[i].computecentre();
			 if(!a)
			 {Map1.remove(c[i]);
				Map1.put(c1[i], 0);
			 }
		 }

	 }

	 while(!Map.containsValue(0))
	
	{	
	 for(Element e:elements)
	 {dist = new ArrayList<>();
		 
	 for(int i=0;i<nc;i++)	
	 {
		dist.add(Math.pow(Math.pow(Math.abs(c[i].xc-e.x), 2)+Math.pow(Math.abs(c[i].yc-e.y), 2), 0.5));
	 }
	 int mn=dist.indexOf(Collections.min(dist));
	    if(!c[mn].celements.contains(e))
			c[mn].insert(e);
		int k=0;
		for(k=0;k<nc;k++)
		 { 
			if(k==mn)
			 continue;
			c[k].remove(e);
		 
		 }

	 }
	 for(int i=0;i<nc;i++)
	 {
		 a=c[i].computecentre();
			if(!a)
			{
				Map.remove(c[i]);
				Map.put(c[i], 0);
			}
	 }
	}
	 System.out.println("Kmeans on 1 Dimension");
	for(int i=0;i<nc;i++)
		c1[i].print();
	 System.out.println("Kmeans on 2 Dimension");
	for(int i=0;i<nc;i++) 
		c[i].print();
	}
}
