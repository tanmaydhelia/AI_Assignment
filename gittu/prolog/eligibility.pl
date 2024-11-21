:- use_module(library(csv)).
:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_dispatch)). % Ensure this is included for http_dispatch
:- use_module(library(http/http_cors)). % Add this module

% Load CSV data into Prolog
load_data(File) :-
    csv_read_file(File, Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

% Rules for eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, _, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, _, Attendance, _),
    Attendance >= 75.

% REST API endpoints
:- http_handler(root(scholarship), scholarship_handler, []).
:- http_handler(root(exam_permission), exam_permission_handler, []).

% API Handlers
scholarship_handler(Request) :-
    http_parameters(Request, [id(Student_ID, [atom])]),
    format('Access-Control-Allow-Origin: http://localhost:8000~n'),
    format('Access-Control-Allow-Methods: GET~n'),
    format('Content-Type: application/json~n~n'),
    (   eligible_for_scholarship(Student_ID)
    ->  reply_json(json{status: "Eligible", for: "Scholarship"}, 
                  [content_type('application/json')])
    ;   reply_json(json{status: "Not Eligible", for: "Scholarship"},
                  [content_type('application/json')])).

exam_permission_handler(Request) :-
    http_parameters(Request, [id(Student_ID, [atom])]),
    format('Access-Control-Allow-Origin: http://localhost:8000~n'),
    format('Access-Control-Allow-Methods: GET~n'),
    format('Content-Type: application/json~n~n'),
    (   permitted_for_exam(Student_ID)
    ->  reply_json(json{status: "Permitted", for: "Exam"},
                  [content_type('application/json')])
    ;   reply_json(json{status: "Not Permitted", for: "Exam"},
                  [content_type('application/json')])).

% Start the HTTP server with HTTP/2 support
start_server(Port) :-
    http_server(http_dispatch, [port(Port), http2(true)]).