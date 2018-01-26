var curr_workout = [];
var curr_exercise = [];

// Show Workouts in the div
function updateWorkouts() {
    var workout_list = "";
    $.get("/workouts/workouts").done(function(data) {
        if (data.length != 0) {
            for (workout in data) {
                workout_list += "<a href='#exercises' id='workoutbtn" + data[workout]['id'] + "' class='dropdown-item' onclick='updateExercises(" +
                                data[workout]['id'] + ")'>" + data[workout]['name'];
                workout_list += "</a>";
            }

        } else {
            workout_list += "<p>No workouts? Add some!</p>";
        }
        $("#workouts-menu").html(workout_list);
    });
}


// Show the exercises in the div
function updateExercises(w_id) {
    var workout_name = "";
    var exer_str = "";
    $.when(
        $.get("/workouts/workouts/" + w_id + "/").done(function(data) {
            curr_workout = data;
            workout_name = data['name'];
        }),
        $.get("/workouts/exercises").done(function(data2) {
            data2.sort(function(a, b) {
                return parseInt(a.order) - parseInt(b.order);
            });
            var repsRange = "";
            var setsRange = "";
            exer_str = "<ul class='list-group'>";
            for (exercise in data2) {
                repsRange = SEtoString(data2[exercise]['repsStart'], data2[exercise]['repsEnd']);
                setsRange = SEtoString(data2[exercise]['setsStart'], data2[exercise]['setsEnd']);
                if ((data2[exercise]['workout_id'].split(',')).indexOf(w_id.toString()) > -1) {
                    exer_str += "<li class='list-group-item'>" +
                                "<a href='#logs' class='btn btn-sm btn-light' onclick='updateLogs(" + data2[exercise]["id"] + ")'>" +
                                data2[exercise]["name"] +
                                "  <span class='badge badge-info'>" +
                                repsRange + "x" + setsRange + "</span>" +
                                "</a>" +
                                "<a href='#' class='btn btn-danger btn-sm float-right' onclick='deleteExercise(" +
                                data2[exercise]['id'] + ", " +
                                w_id + ")'>Delete</a></li>";
                }
            }
            exer_str += "</ul>";
        })
    ).then(function() {
        $("#work-head").attr({'class': 'invisible'});
        $("#exercise-sec").attr({'class': 'col visible'});
        $("#log-sec").attr({'class': 'row invisible'});
        console.log("Got Exercises for Workout " + w_id);
        $("#logs").html("");
        if (exer_str == "<ul class='list-group'></ul>") {
            $("#exercises").html("<p>No exercises, add some!</p>");
        } else {
            $("#exercises").html(exer_str);
        }
        $("#workout_name").html("<button href='#' class='btn btn-outline-danger float-right mt-2' onclick='deleteWorkout(" +
                                w_id + ")'>Delete " + workout_name + "</button>")
        $("#id_workout_id").val(w_id);
        $("#id_exist_workout_id").val(w_id);
        addListOfExistExer(w_id);
    });
}

// Show the logs in the div
function updateLogs(e_id) {
    var log_str = "";
    $.when(
        $.get("/workouts/logs").done(function(data3n) {
            var data3 = [];
            for (x in data3n) {
                if (data3n[x]['exercise_id'] == e_id) {
                    data3.push(data3n[x]);
                }
            }
            // Sort by most recent
            data3.sort(function (b, a) {
                return a.date.localeCompare(b.date);
            });
            // HTML code for the card/form log
            var log_mr = "";
            if (data3.length == 0) {
                $("#log_most_recent").html("No logs? add some!");
            } else {
            log_mr +=
    "<div class='row mb-2'>" +
        "<div class='col-sm'>" +
            "<div class='card'>" +
                "<div class='card-body'>" +
                    "<h4 class='card-title'>" + data3[0]["weight"] + "</h4>" +
                    "<h6 class='card-subtitle mb-2 text-muted'>" + data3[0]["date"] + "</h6>" +
                    "<p class='card-text'>" + formatRepsHTML(data3[0]["reps"]) + "</p>" +
                    "<form onSubmit='return false;' class=' card-text form-row mt-2'>" +
                        "<input type='number' pattern='\d*' id='set_num" + data3[0]['id'] +
                        "' class='form-control form-control-sm col mr-2 mb-2' placeholder='Reps' required>" +
                        "<button type='button' class='btn btn-primary btn-sm col mb-2' onclick='addSet(" +
                        data3[0]['id'] + ", " + e_id + ")'" +
                        ">Add Set</button>" +
                        "<div class='w-100'></div>" +
                        "<button type='button' class='btn btn-warning btn-sm col' onclick='deleteLastSet(" +
                        data3[0]['id'] + ", " + e_id + ")'" +
                        ">Remove Last Set</button>" +
                        "<a href='#' class='btn btn-danger btn-sm col ml-2' onclick='deleteLog(" +
                        data3[0]['id'] + ', ' + e_id + ")'>Delete</a>" +
                    "</form>" +
                "</div>" +
            "</div>" +
        "</div>" +
    "</div>";
            $("#log_most_recent").html(log_mr);
            }
            var log_thead = "<thead><tr>";
            log_thead +=
            "<th>Date</th>" +
            "<th>Weight</th>" +
            "<th>Sets/Reps</th></tr></thead>";
            var log_tbody = "<tbody>";
            for (log in data3) {
                if (data3[log]['exercise_id'] == e_id) {
                    //console.log("added log to table for exercise " + e_id);
                    log_tbody +=
                    "<tr><th>" + data3[log]['date'] + "</th>" +
                    "<td>" + data3[log]['weight'] + "</td>" +
                    "<td>" + data3[log]['reps'] + "</td></tr>";
                } else {
                    console.log(data3[0]['exercise_id']);
                }
            }
            log_tbody += "</tbody>";
            log_str += "<table class='table'>" + log_thead + log_tbody + "</table>";
        })
    ).then(function() {
        $("#log-sec").attr({'class': 'row visible'});
        $("#logs").html(log_str);
        $("#id_exercise_id").val(e_id);
    });

}

// Delete logs with an e_id of an exercise that doesn't exist
function deleteZombieLogs(e_id) {
    $.get("/workouts/logs").done(function(data) {
        for (log in data) {
            if (data[log]['exercise_id'] == e_id) {
                deleteLog(data[log]['id'], e_id);
            }
        }
    });
}

function deleteZombieExercises(w_id) {
    $.get("/workouts/exercises").done(function(data) {
        for (exercise in data) {
            if (data[exercise]['workout_id'].split(",").indexOf(w_id.toString()) > -1) {
                deleteExercise(data[exercise]['id'], w_id);
                console.log('got here');
            } else {
                console.log('failed case');
            }
        }
    });
}

$("#submit").click(function() {
    var form_data = $("#workout_form").serialize();
    $.post("/workouts/workouts/", form_data).done(function() {
         updateWorkouts();
         console.log("Added workout");
    });
});

$("#submit2").click(function() {
    var form2_data = $("#exercise_form").serialize();
    $.post("/workouts/exercises/", form2_data).done(function() {
        updateExercises($("#id_workout_id").val());
        console.log("Added exercise");
    }).fail(function(xhr, status, error) {
        console.log("some error");
    });
});

$("#submit_ee").click(function() {
    // Get the form data from the 'Existing Exercise' form.
    var array_data = $("#existing_exer_form").serializeArray();

    // Get request for the workout selected
    $.get("/workouts/exercises/" + array_data[1]['value'] + '/').done(function(data) {

        // Operations to add the current workout to the list of workout ids in the exercise
        var old_workout = data['workout_id'];
        old_workout = old_workout.split(',');
        old_workout.push(array_data[3]['value']);
        var new_workout = old_workout.join();

        // serialized data sent in the PUT ajax request
        var dataPUT = "name=" + data['name'] +
                 "&repsStart=" + data['repsStart'] +
                 "&repsEnd=" + data['repsEnd'] +
                 "&setsStart=" + data['setsStart'] +
                 "&setsEnd=" + data['setsEnd'] +
                 "&order=" + parseInt(array_data[2]['value']) +
                 "&workout_id=" + new_workout;

        // The Ajax request itself.
        $.ajax({
           url: '/workouts/exercises/' + data['id'] + '/',
           type: 'PUT',
           beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
           },
           data: dataPUT,
           success: function(response) {
                console.log("added existing exercise to this workout");
                updateExercises(parseInt(array_data[3]['value']));
           }
        });
    });
});

$("#submit3").click(function() {
    var form3_data = $("#log_form").serialize();
    $.post("/workouts/logs/", form3_data).done(function() {
        updateLogs($("#id_exercise_id").val());
        console.log("Added log");
    }).fail(function(xhr, status, error) {
        console.log("some error");
    });
});

$("#log_form").keypress(function(e) {
    if(e.which == 13) {
        $("#submit3").click();
    }
});

$("#exercise_form").keypress(function(e) {
    if(e.which == 13) {
        $("#submit2").click();
    }
});

$("#workout_form").keypress(function(e) {
    if(e.which == 13) {
        $("#submit").click();
    }
});

$(".set_form").keypress(function(e) {
    if(e.which == 13) {
        $(".submit_set").click();
    }
});

// Default Django function to get the CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteListOfExistExer(e_id) {
    $("#id_exercise option[value='" + e_id + "']").remove();
}

function rmLast(s) {
    s_array = s.split("-");
    s_array.pop();
    x = s_array.join("-");
    return x;
}

function formatRepsHTML(s) {
    var s_array = s.split("-");
    var h_str = "<table class='table'>";
    var h_str_head = "<thead><tr><th>Set</th>";
    var h_str_body = "<tbody><tr><th>Reps</th>";
    for (var i = 1; i < s_array.length+1; i++) {
        h_str_head += "<th>" + i + "</th>";
        h_str_body += "<td>" + s_array[i-1] + "</td>";
    }
    h_str_head += "</tr></thead>";
    h_str_body += "</tr></tbody>";
    h_str += h_str_head + h_str_body + "</table>";
    return h_str;
}

function insertToday() {
    $("#id_date").val(moment().format('YYYY-MM-DD'));
}

function SEtoString(rs, re) {
    var range = "";
    if (rs == re) {
        range = rs;
    } else {
        range = rs + "-" + re;
    }
    return range;
}