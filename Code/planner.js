
majorCourses = [];
minorCourses = [];
otherCourses = [];
majors = [];
minors = [];
$(document).ready(function(){

    $.ajax({
        url: "majors.php",
        dataType: "json",
        type: 'post',
        success: function (response) {
            majors = response;
            var options = "";
            $.each(response, function(k, v) {

                if(k.length > 25){
                    var str = k.substr(0,24) + "...";
                }
                else {
                    var str = k;
                }
                options += "<option value='" + k + "'>" + str + "</option>";
            });
            $("#major").append(options);
        },
        error: function (error) {
            console.log(error);
        }
    });

    $.ajax({
        url: "minors.php",
        dataType: "json",
        type: 'post',
        success: function (response) {
            minors = response;
            var minorOptions = "";

            $.each(response, function(k, v) {
                if(k.length > 25){
                    var str = k.substr(0,24) + "...";
                }
                else {
                    var str = k;
                }
                minorOptions += "<option value='" + k + "'>" + str + "</option>";
            });
            $("#minor").append(minorOptions);
        },
        error: function (error) {
            console.log(error);
        }
    });

})
function getMajorCourses(value) {

    var arr = [];
    $.each(majors[value].subjects, function (k, v) {
        arr.push(v);
    });
    $("#maLink").remove();
    $("#majorLink").append("<a href='" + majors[value].uri + "' id='maLink' target='_blank'> " + value + " </a>");

    arr.sort();

    $.ajax({
        url: "courses.php",
        dataType: "json",
        data: {
            codes: JSON.stringify(arr)
        },
        type: 'post',
        success: function (response) {

            majorCourses = response;
            var list = makeCourseList(response, "major");
            $("#major-list").empty();
            $("#major-list").append(list);

        },
        error: function (error) {
            console.log(error);
        }
    });
}

function getMinorCourses(value) {

    var arr = [];
    $.each(minors[value].subjects, function (k, v) {
        arr.push(v);
    });

    $("#miLink").remove();
    $("#minorLink").append("<a href='" + minors[value].uri + "' id='miLink' target='_blank'> " + value + " </a>")

    arr.sort();
    $.ajax({
        url: "courses.php",
        dataType: "json",
        data: {
            codes: JSON.stringify(arr)
        },
        type: 'post',
        success: function (response) {
            minorCourses = response;
            var list = makeCourseList(response, "minor");
            $("#minor-list").empty();
            $("#minor-list").append(list);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function getSearchCourses(selectedValue) {

    var arr = selectedValue.split(" ");

    if(!isNaN(arr[1])) {
        $.ajax({
            url: "searchSpecificCourse.php",
            dataType: "json",
            type: 'post',
            data: {
                search: JSON.stringify(arr)
            },
            success: function (response) {

                otherCourses = response;
                var list = makeCourseList(response, "search");
                $("#other-list").empty();
                $("#other-list").append(list);

            },
            error: function (error) {
                console.log(error);
            }
        });
    }
    else {
        $.ajax({
            url: "search.php",
            dataType: "json",
            type: 'post',
            data: {
                search: selectedValue
            },
            success: function (response) {

                otherCourses = response;
                var list = makeCourseList(response, "search");
                $("#other-list").empty();
                $("#other-list").append(list);

            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function removeYear() {
    $('#years').children().last().remove();
}

function addYear() {
    var id = $('#years').children().last().attr('id');
    var numYears = $('#years').children().length;

    if(numYears > 12){
        alert("Max number of years reached!");
        return;
    }
    if(isNaN(id)){
        id = 2018;
    }
    else{
        id = parseInt(id) + 1;
    }


    var str = " <div class='row' id='" + id + "'>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Fall " + id + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Spring " + (id+1) + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Summer " + (id+1) + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                </div>"

    $('#years').append(str);
}


function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

function courseInfo(element){
    var id = element.id;
    id = id.split(" ");

    if(id[0] === "major"){
        var course = majorCourses[id[2]].courseName + " " + majorCourses[id[2]].courseNum;
        var title = majorCourses[id[2]].title;
        var description = majorCourses[id[2]].description;
        var prereqs = majorCourses[id[2]].prerequisite;
        var hours = majorCourses[id[2]].creditHours;
    }
    else if(id[0] === "minor"){
        var course = minorCourses[id[2]].courseName + " " + minorCourses[id[2]].courseNum;
        var title = minorCourses[id[2]].title;
        var description = minorCourses[id[2]].description;
        var prereqs = minorCourses[id[2]].prerequisite;
        var hours = minorCourses[id[2]].creditHours;
    }
    else {
        var course = otherCourses[id[2]].courseName + " " + otherCourses[id[2]].courseNum;
        var title = otherCourses[id[2]].title;
        var description = otherCourses[id[2]].description;
        var prereqs = otherCourses[id[2]].prerequisite;
        var hours = otherCourses[id[2]].creditHours;
    }


    var str = " <h6>Course:</h6>" + " " + course + "<br>\n" +
        "                <h6>Title: </h6>" + " " + title + "<br>\n" +
        "                <h6>Credit Hours: </h6>" + " " + hours + "<br>\n" +
        "                <h6>Pre-Requisites: </h6><br>" + prereqs + "<br>\n" +
        "                <h6>Description: </h6><br>" + description + "<b"

    $('#courseInfo').empty();
    $('#courseInfo').append(str);
}


function makeCourseList(response, prefix){
    var list = "";
    var count = 0;
    $.each(response, function(k, v) {
        list+=  "<li draggable='true' ondragstart='drag(event)' id='" + prefix + " " + count + "'>" +
            "<div class='courseList'>" +
            v.courseName + " " + v.courseNum + "<img draggable='false' id='" + prefix + " img " + count++ + "' class='info' src='Info.png' " +
            "onclick='courseInfo(this)'> </div></li>\n"

    });

    return list;
}


