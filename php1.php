<?php
require("connect_db.php");

$sql = "SELECT id, fname, lname, age, sex, marry_status FROM survey";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    if($row["sex"]=="M"){
      if($row["age"]>=15){
      echo " นาย  ".$row["fname"] .  " " . $row["lname"]. "   -age  " . $row["age"] ."  -status  ". $row["marry_status"]. "<br>";
      }
      else{
        echo " ด.ช. ".$row["fname"] .  " " . $row["lname"]. "   -age  " . $row["age"] ."  -status  " .$row["marry_status"] ."<br>";
      }
    }else{
      if($row["age"]>=15){
          if($row["marry_status"]=="M"){
            echo " นาง  ".$row["fname"] .  " " . $row["lname"]. "   -age  " . $row["age"] ."  -status  ". $row["marry_status"]. "<br>";
          }else{
            echo " น.ส.  ".$row["fname"] .  " " . $row["lname"]. "   -age  " . $row["age"] ."  -status  ". $row["marry_status"]. "<br>";
          }
         
      }
      else{
        echo " ด.ญ.  ".$row["fname"] .  " " . $row["lname"]. "   -age  " . $row["age"] ."  -status  ". $row["marry_status"]. "<br>";
      }
    }
  }
    
    

} else {
  echo "0 results";
}
$conn->close();
?>
เขียนถึง Kittipong Wiangwised

