*kgm* is command-line processor utility which allows user to control and manipulate K<span/>GM-controlled graphs in backend graph database.

## Installation

### local `pip install`

```
$ python3 -m venv ~/venv/kgm
$ source ~/venv/kgm/bin/activate
$ pip install py-packages/kgm
```

## K<span/>GM path
KGM provides the way to organize the knowledge graphs in the way similar to files in traditional filesystem.

One of the way to populate KG is to dowload .ttl file using `kgm import` command:
```console
$ kgm import /alice-bob.shacl http://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.shacl.ttl
/alice-bob.shacl http://www.geisel-software.com/RDF/KGM#SHACLGraph--40c4faaf-f311-4112-bfec-a945b4f7cdbb

$ kgm import /alice-bob http://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl
/alice-bob http://www.geisel-software.com/RDF/KGM#DataGraph--5f90e074-5582-4ba6-bcf5-67dc55ed4754

$ kgm ls
        kgm_path                                                  g
0        "/alice-bob"  kgm:DataGraph--5f90e074-5582-4ba6-bcf5-67dc55e...
1  "/alice-bob.shacl"  kgm:SHACLGraph--40c4faaf-f311-4112-bfec-a945b4...
```

To access the KG one can use SPARQL console attached to backend database. Using `kgm query` command it is possible to issue SPARQL query:
```console
kgm query -Q '
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

select ?human ?h_name
where {
 ?g kgm:path "/alice-bob"
 graph ?g {
  ?human rdf:type ab:Human .
  ?human ab:name ?h_name .
 }
}
'
```

Output:
```sh
        human     h_name
0    ab:alice    "Alice"
1      ab:bob      "Bob"
2  ab:charlie  "Charlie"
```


## Examples
### Alice-Bob
data files location:

 - [ab.data.ttl] -- data RDF triples
 - [ab.shacl.ttl] -- SHACL structure

Alice-Bob queries:

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

select ?owner_name ?pet_name ?pet_class
where {
  ?g kgm:path "/alice-bob"
  graph ?g {
      ?pet rdf:type ?pet_class;
           ab:name ?pet_name;
           ab:ownedBy ?owner;
      .
      ?owner ab:name ?owner_name .
  }
}
```

### NorthWind

[NorthWind](https://en.wikiversity.org/wiki/Database_Examples/Northwind) is sample SQL database. We will convert to RDF and then load into KGM-controlled Fuseki server. See also [Neo4J northwind example at github](https://github.com/neo4j-graph-examples/northwind/tree/main)


data file locations:

- [northwind-sqlite.sql] -- Northwind data as SQL inserts
- [northwind.shacl.ttl] -- SHACL schema of Northwind

The script [build-rdf.py](examples/northwind/build-rdf.py) uses rdflib python package.

```console
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/nortwind-sqlite.sql
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/northwind.shacl.ttl
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/build-rdf.py
$ sqlite3 northwind.sqlitedb < northwind-sqlite.sql
$ python build-rdf.py > northwind.data.ttl
```

```console
$ kgm import /NorthWind northwind.data.ttl
$ kgm import /NorthWind.shacl northwind.shacl.ttl
$ kgm validate /NorthWind.shacl /NorthWind
```

#### Query examples

##### Counts
```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

select ?order (count(?od) as ?c)
where {
  ?g kgm:path "/NorthWind" .
  graph ?g {
    ?order rdf:type nw:Order;
    	   nw:order_detail ?od
  }
}
group by ?order
order by desc(?c)
```

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

select ?c (count(*) as ?cc) {
 select ?order (count(?od) as ?c)
 where {
  ?g kgm:path "/NorthWind" .
  graph ?g {
   ?order rdf:type nw:Order;
          nw:order_detail ?od
  }
 }
 group by ?order
 # order by desc(?c)
}
group by ?c
```

##### Get all products and their suppliers

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

select ?pn ?suppl_n
where {
 ?g kgm:path "/NorthWind" .
 graph ?g {
  ?p rdf:type nw:Product; nw:supplier ?suppl; nw:productname ?pn.
  ?suppl nw:suppliername ?suppl_n
 }
}
```

```sql
SELECT Products.ProductName, Suppliers.SupplierName
FROM Products
JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID;
```

##### List all orders with customer and employee information

```sparql
select ?orderid ?company_name ?employee_lastname ?orderdate
where {
  ?g kgm:path "/NorthWind" .
  graph ?g {
    ?customer rdf:type nw:Customer; nw:customername ?company_name.
    ?order nw:customer ?customer; nw:orderdate ?orderdate; nw:orderid ?orderid.
    ?order nw:employee ?employee.
    ?employee nw:lastname ?employee_lastname
  }
}
```

```sql
SELECT Orders.OrderID, Customers.CompanyName AS Customer, Employees.LastName AS Employee, Orders.OrderDate
FROM Orders
INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
INNER JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID;
```

##### Find the total number of orders placed by each customer
```sql
SELECT Customers.CompanyName, COUNT(Orders.OrderID) AS TotalOrders
FROM Customers
INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CompanyName
ORDER BY TotalOrders DESC;
```

##### List products that have never been ordered
```sql
SELECT ProductName
FROM Products
WHERE ProductID NOT IN (SELECT ProductID FROM [Order Details]);
```

##### Get the top 5 customers with the highest number of orders
```sql
SELECT Customers.CompanyName, COUNT(Orders.OrderID) AS OrderCount
FROM Customers
INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CompanyName
ORDER BY OrderCount DESC
LIMIT 5;
```

##### Find the employee who has processed the most orders
```sql
SELECT Employees.LastName, COUNT(Orders.OrderID) AS OrdersProcessed
FROM Employees
INNER JOIN Orders ON Employees.EmployeeID = Orders.EmployeeID
GROUP BY Employees.LastName
ORDER BY OrdersProcessed DESC
LIMIT 1;
```

##### Get the total sales for each product
```sql
SELECT Products.ProductName, SUM([Order Details].UnitPrice * [Order Details].Quantity) AS TotalSales
FROM Products
INNER JOIN [Order Details] ON Products.ProductID = [Order Details].ProductID
GROUP BY Products.ProductName
ORDER BY TotalSales DESC;
```

##### Find the average freight cost per order
```sql
SELECT AVG(Freight) AS AverageFreight
FROM Orders;
```

##### Get the total number of products supplied by each supplier
```sql
SELECT Suppliers.CompanyName, COUNT(Products.ProductID) AS TotalProducts
FROM Suppliers
INNER JOIN Products ON Suppliers.SupplierID = Products.SupplierID
GROUP BY Suppliers.CompanyName;
```

##### List all orders shipped to Germany
```sql
SELECT Orders.OrderID, Orders.OrderDate, Orders.ShipCountry
FROM Orders
WHERE Orders.ShipCountry = 'Germany';
```
