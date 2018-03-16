<?php
	
	$codes = json_decode($_POST['codes']);
	$rows = array();
	foreach($codes as $code) {

		$sql = new mysqli("cse.unl.edu", "apages", "Wtpt4R", "apages");

		$qry = "SELECT Course.title AS title, description, prerequisite, creditHours, courseNum FROM Course JOIN Subject ON Course.subject_fk = Subject.subject_key WHERE subjectId = ?";
		$qry = $sql->prepare($qry);
		$qry->bind_param("s", $code);

		$qry->execute();
		$result = $qry->get_result();

	//while($row = mysqli_fetch_assoc($result)) {
	//	echo $row["title"];
	//}

		while ($row = mysqli_fetch_assoc($result)) {
			$rows[] = array(
				'title' => $row['title'],
				'description' => $row['description'],
				'prerequisite' => $row['prerequisite'],
				'creditHours' => $row['creditHours'],
				'courseName' => $code,
				'courseNum' => $row['courseNum']
			);
		}


	}
	mysqli_close($sql);
	echo json_encode($rows);
?>
