*kgm* is command-line processor utility which allows user to control and manipulate K<span/>GM-controlled graphs in backend graph database.

## Installation

### local `pip install`

```
$ python3 -m venv ~/venv/kgm
$ source ~/venv/kgm/bin/activate
$ pip install py-packages/kgm
```

## How K<span/>GM manages graphs?
KGM provides the way to organize the knowledge graphs in the way similar to files in traditional filesystem. It does that using particular feature which is a part of RDF definitions: fourth entry of RDF triple.

### RDF quads

That's right - there are four entries available in RDF triples. Fourth entry provides the way to assign triple to particular graph. Consider [the example](https://www.w3.org/TR/rdf12-n-quads/#simple-triples) of quad:

```
@prefix e: <http://example.org/#> .
@prefix r: <http://www.perceive.net/schemas/relationship/> .
e:spiderman r:enemyOf e:green-goblin <http://example.org/graphs/spiderman> .
```

Fourth entry meaning that the triple belong to graph `http://example.org/graphs/spiderman`. This graph URI can be used to specify graph in SPARQL statement using `graph` keyword:

```sparql
select ?s ?p ?o where {
 graph <http://example.org/graphs/spiderman> {
  ?s ?p ?o
 }
}
```
SPARQL assumption is there are query clauses which are not in `graph` group then query will work with triples from default graph.


### KGM default graph

KGM uses default graph to store triples to describe all user graphs. E.g:
```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
@prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
@prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

kgm:Graph--27f7b699-8054-49a3-88c6-e80636ae9823 rdf:type kgm:Graph .
kgm:Graph--27f7b699-8054-49a3-88c6-e80636ae9823 kgm:path "/alice-bob" .
```

It allows to use `graph` clause in SPARQL to address particular user graph by `kgm:path`:

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

select * where {
 ?g kgm:path "/alice-bob" .
 graph ?g {
  ?s ?p ?o
 }
}
```

## KGM commands

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

Import commands:

```
kgm import /alice-bob.shacl https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.shacl.ttl
kgm import /alice-bob https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl
```

#### Alice-Bob queries

##### Alice

=== "long"
    ```sparql
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

    select ?h_name ?city ?f_name ?f_city
    where {
     ?g kgm:path "/alice-bob"
     graph ?g {
      bind("Alice" as ?h_name)
      ?human ab:name ?h_name.
      ?human ab:livesIn ?loc.
      ?human ab:friendOf ?friend.
      ?loc ab:city-name ?city.
      ?friend ab:name ?f_name.
      ?friend ab:livesIn ?f_loc.
      ?f_loc ab:city-name ?f_city
     }
    }
    ```
=== "short"
    ```sparql
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

    select ?h_name ?city ?f_name ?f_city {
     ?g kgm:path "/alice-bob"
     graph ?g {
      bind("Alice" as ?h_name)
      ?human ab:name ?h_name; ab:livesIn ?loc;
             ab:friendOf ?friend.
      ?loc ab:city-name ?city.
      ?friend ab:name ?f_name; ab:livesIn ?f_loc.
      ?f_loc ab:city-name ?f_city
     }
    }
    ```
    
##### Pets


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
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/northwind-sqlite.sql
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
=== "SPARQL"
    ```sparql
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

    select ?order (count(?od) as ?c) where {
     ?g kgm:path "/NorthWind" .
     graph ?g {
      ?order rdf:type nw:Order;
      nw:order_detail ?od
     }
    }
    group by ?order
    order by desc(?c)
    ```
=== "SQL"
    ```sql
    select OrderID, count(*) 
    from OrderDetails 
    group by OrderID 
    order by count(*);
    ```

##### Counts 2

=== "SPARQL"
    ```sparql
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

    select ?items_count (count(*) as ?c) {
     select ?order (count(?od) as ?items_count)
     where {
      ?g kgm:path "/NorthWind" .
      graph ?g {
       ?order rdf:type nw:Order;
              nw:order_detail ?od
      }
     }
     group by ?order
    }
    group by ?items_count
    order by ?items_count
    ```
=== "SQL"
    ```sql
    select items_count, count(*)
    from (
     select OrderID, count(*) as items_count
     from OrderDetails
     group by OrderID
    )
    group by 1
    order by 1;
    ```

##### Get all products and their suppliers

=== "SPARQL"
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
=== "SQL"
    ```sql
    SELECT Products.ProductName, Suppliers.SupplierName
    FROM Products
    JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID;
    ```


##### List all orders with customer and employee information

=== "SPARQL"
    ```sparql
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

    select ?orderid ?customer_name ?employee_lastname ?orderdate
    where {
     ?g kgm:path "/NorthWind" .
     graph ?g {
      ?customer rdf:type nw:Customer; nw:customername ?customer_name.
      ?order nw:customer ?customer; nw:orderdate ?orderdate; nw:orderid ?orderid;
             nw:employee ?employee.
      ?employee nw:lastname ?employee_lastname
     }
    }
    ```
=== "SQL"
    ```sql
    SELECT Orders.OrderID, Customers.CustomerName AS Customer,
    	   Employees.LastName AS Employee, Orders.OrderDate
    FROM Orders
    INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    INNER JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID;
    ```

<!--
##### WIP - Find the total number of orders placed by each customer
=== "SPARQL"
    ```sparql
    # BUG in Fuseki2
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
    prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

    select *
    {
     ?g kgm:path "/NorthWind" .
     {
      select (count(?order) as ?c) {
      graph ?g {
        ?customer rdf:type nw:Customer.
        ?order nw:customer ?customer.
       }
      }
      group by ?customer
     }
     ?customer rdf:type ?cn
    }
    ```
=== "SQL"
    ```sql
    SELECT counts.CustomerID, CustomerName, TotalOrders
    FROM (
     SELECT Customers.CustomerID, COUNT(Orders.OrderID) AS TotalOrders
     FROM Customers
     INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
     GROUP BY Customers.CustomerID
    ) counts
    JOIN Customers on Customers.CustomerID = counts.CustomerID
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
-->
