from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


#list the assignments based on the status of the assignments
@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.accept_urlparams
@decorators.auth_principal
def list_assignments(p,url_params):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id,url_params.get('state'))
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)
    

#update the assignments grades
@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def update_grade(p,incoming_payload):
    """update grade"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    grade_assignments = Assignment.update_grade(
        _id=grade_assignment_payload.id,
        principal=p,
        grade=grade_assignment_payload.grade
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(grade_assignments)
    return APIResponse.respond(data=graded_assignment_dump)

    