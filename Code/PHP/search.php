<?php

	//error_reporting(E_ALL); ini_set('display_errors', 1);
	
	$search = "%" . $_POST['search'] . "%";

	$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");

	$qry = "SELECT c.title, c.description, c.prerequisite, c.creditHours, c.courseNum, s.subjectId, a1.aceNum, a2.aceNum ".
			"FROM Course c JOIN Subject s ON c.subject_fk = s.subject_key ".
			"LEFT JOIN Ace AS ace1 ON c.ace_1_fk = a1.ace_key ".
			"LEFT JOIN Ace AS ace2 ON c.ace_2_fk = a2.ace_key ".
			"WHERE UPPER(s.subjectId) LIKE UPPER(?) ".
			"OR UPPER(c.title) LIKE UPPER(?) ".
			"OR UPPER(CONCAT(s.subjectID,c.courseNum)) LIKE UPPER(?)";
	$qry = $sql->prepare($qry);
	$qry->bind_param('sss', $search, $search, $search);

	$qry->execute();
	$result = $qry->get_result();

	$sql->close();

	while ($row = mysqli_fetch_assoc($result)) {
		$rows[] = array(
			'title' => $row['c.title'],
			'description' => $row['c.description'],
			'prerequisite' => $row['c.prerequisite'],
			'creditHours' => $row['c.creditHours'],
			'courseNum' => $row['c.courseNum'],
			'courseName' => $row['s.subjectId'],
			'ace1' => $row['a1.aceNum'],
			'ace2' => $row['a2.aceNum']
		);
	}

	echo json_encode($rows);
?>
