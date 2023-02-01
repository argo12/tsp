test <- function(n,a,g) {
  # we can add our own integrity checks
  if(g>4 || g<0)  stop("GPA must be between 0 and 4")
  value <- list(name = n, age = a, GPA = g)
  # class can be set using class() or attr() function
  attr(value, "class") <- "student"
  value
}

# TODO replace range with seq

Node <- function(
  size, cost, sorted_edges, 
  all_sorted_edges, parent_constr, 
  extra_consrt=NULL
  ){
  
  
  removeEdges <- function( constraints ){
    
    for (i in seq(0, size-1)){
      t = 0
      for (j in seq(0,size-1)){
        if( i != j  &  constraints [i][j] == 1) {
          t = t +1
        }
      }
      
      if (t >= 2) {
       for( j in seq(0,size-1)){} 
          if (constraints [i][j] == 2){
            constraints [i][j] = 0
            constraints [j][i] = 0
          }
        }
      
      
    }
    
    
    for( i in seq(0, size-1 )){
      for( j in seq(0, size-1 )){
        t = 1
        prev = i
        fr =  j
        cycle = FALSE
        nextOne = next_one(prev ,fr , constraints )
      }
    }
      
    
  }
  
  next_one <- function(prev ,fr , constraints ){
    
  }
  
  
  value <-  list( size = size, cost= cost, sorted_edges = sorted_edges,
                  all_sorted_edges = all_sorted_edges, parent_constr= parent_constr,
                  extra_consrt= extra_consrt)
  
  attr(value, "class") <- "Node"
  value
}

compute_lower_boud <- function(Node) {
  lb <- 0
  for (  i in range(Node$size)){
    lower <- 0
    t <- 0
    for (j in Node$size){
      if (Node$constraints [i][j] == 1){
        lower <- Node$costs[i][j] + lower
        t = t + 1
      }

        tt = 0
        while(t < 2){
          shortest <- Node$sortedEdges [i][tt]
          if(Node$constraints [i][ shortest ] == 2){
            lower = lower + self.costs[i][shortest]
            t = t + 1
          }
          tt  = tt + 1
          if (tt >= Node$size){
            lower = Inf
            break
            
            }
       
      }
    }
    
    lb = lower + lb
  }
  
  return(lb)
}


determine_constr <- function(Node , parent_constr ){
  constraints <- parent_constr
  if (is.null(Node$extra_constr)){
    return(constraints)
  }
  
  fr <- Node$extra_constr[0]
  to <- Node$extra_constr[1]
  
  constraints[fr][to] <- Node$extra_constr[2]
  constraints[to][fr] <- Node$extra_constr[2]
  
  for (i in range (2)) {
    
    constraints =  Node$removeEdges ( constraints )
    constraints =  Node$addEdges ( constraints )
    
    }
  
  return(list(Node, constraints))
  
}


# tst <- function(Node) {
#   
#   Node$size <- 1221
#   return(Node)
# }
# 
# 
# <- tst(s)
