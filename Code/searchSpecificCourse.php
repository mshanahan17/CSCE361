<?php

//error_reporting(E_ALL); ini_set('display_errors', 1);

$search = json_decode($_POST['search']);
$search1 = "%".$search[0]."%";
$search2 = "%".$search[1]."%";
$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");

$qry = "SELECT Course.title AS title, description, prerequisite, creditHours, courseNum, subjectId FROM Course JOIN Subject ON Course.subject_fk = Subject.subject_key WHERE UPPER(subjectId) LIKE UPPER(?) AND Course.courseNum LIKE ?";
$qry = $sql->prepare($qry);
$qry->bind_param('ss', $search1, $search2);

$qry->execute();
$result = $qry->get_result();

$sql->close();

while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = array(
        'title' => $row['title'],
        'description' => $row['description'],
        'prerequisite' => $row['prerequisite'],
        'creditHours' => $row['creditHours'],
        'courseNum' => $row['courseNum'],
        'courseName' => $row['subjectId']
    );
}

echo json_encode($rows);
?>