<?php
	
	$codes = json_decode($_POST['codes']);
	$rows = array();
	foreach($codes as $code) {

		$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");

		$qry = "SELECT c.title, c.description, c.prerequisite, c.creditHours, c.courseNum, a1.aceNum, a2.aceNum FROM Course c JOIN Subject ON c.subject_fk = Subject.subject_key LEFT JOIN Ace AS a1 ON c.ace_1_fk = a1.ace_key LEFT JOIN Ace AS a2 ON c.ace_2_fk = a2.ace_key WHERE subjectId = ?";
		
		$qry = $sql->prepare($qry);
		$qry->bind_param("s", $code);

		$qry->execute();
		$result = $qry->get_result();

	//while($row = mysqli_fetch_assoc($result)) {
	//	echo $row["title"];
	//}

		while ($row = mysqli_fetch_assoc($result)) {
			$rows[] = array(
				'title' => $row['c.title'],
				'description' => $row['c.description'],
				'prerequisite' => $row['c.prerequisite'],
				'creditHours' => $row['c.creditHours'],
				'courseName' => $code,
				'courseNum' => $row['c.courseNum'],
				'ace1' => $row['a1.aceNum'],
				'ace2' => $row['a2.aceNum']
			);
		}


	}
	mysqli_close($sql);
	echo json_encode($rows);
?>
