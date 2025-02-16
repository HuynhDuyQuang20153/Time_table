// "refesh" - Nút refresh có data-refresh-button
document.querySelectorAll('[data-refresh-button]').forEach(button => {
    button.addEventListener('click', function () {
        location.reload(true); // Thực hiện reload bỏ qua cache
    });
});


function updateFormFields(result){
    if (!result || result.length === 0) {
        document.getElementById('Period_from').value = '';
        document.getElementById('Period_to').value = '';
        document.getElementById('Date_start').value = '';
        document.getElementById('Date_end').value = '';
        document.getElementById('subject').value = '';
        document.getElementById('class_code').value = '';
        document.getElementById('date_week').value = '';
        document.getElementById('Learning_facility').value = '';
        document.getElementById('Room').value = '';
        document.getElementById('Teacher').value = '';
        document.getElementById('Team').value = '';
        document.getElementById('Code_online').value = '';
        document.getElementById('Learning_software').value = '';
        let selectedTypeClass = document.querySelector(`input[name="type_class"]:checked`);
        if (selectedTypeClass) selectedTypeClass.checked = false;
        document.querySelectorAll('input[name="suspension"]').forEach(checkbox => {
            checkbox.checked = false;
        });

    } else {
        document.getElementById('error_notify_edit_data').textContent = '';
        document.getElementById('Period_from').value = result.data[0].period_from;
        document.getElementById('Period_to').value = result.data[0].period_to;
        document.getElementById('Date_start').value = result.data[0].date_start;
        document.getElementById('Date_end').value = result.data[0].date_end;
        document.getElementById('class_code').value = result.data[0].class_code;
        document.getElementById('date_week').value = result.data[0].date_week;
        document.getElementById('Learning_facility').value = result.data[0].learning_facility;
        document.getElementById('Room').value = result.data[0].room;
        document.getElementById('Teacher').value = result.data[0].teacher_name;
        document.querySelector(`input[name="type_class"][value="${result.data[0].type_class}"]`).checked = true;
        document.getElementById('Team').value = result.data[0].team;
        document.getElementById('Code_online').value = result.data[0].code_online;
        document.getElementById('Learning_software').value = result.data[0].learning_software;
        if (result.data[0].suspension_status !== "") {
            const checkbox = document.querySelector(`input[name="suspension"][value="${result.data[0].suspension_status}"]`);
            
            if (checkbox) {
                checkbox.checked = true;  // Đánh dấu checkbox nếu tìm thấy
            }
        } else {
            // Nếu giá trị là chuỗi rỗng, bỏ chọn tất cả checkbox
            document.querySelectorAll('input[name="suspension"]').forEach(checkbox => {
                checkbox.checked = false;
            });
        }
    }
}

function getSelectedRadioValue() {
    const radios = document.querySelectorAll('input[name="type_class"]');
    for (const radio of radios) {
        if (radio.checked) {
            return radio.value; 
        }
    }
    return null; 
}

function delete_all_data() {
    const form = document.getElementById('submit_form_new_data');
    document.getElementById('error_notify_new_data').textContent = '';
    form.reset();
}



document.addEventListener('DOMContentLoaded', function() {
    // kiểm tra điều kiện submit
    const check_value_form = document.getElementById("submit_form_new_data");
    check_value_form.addEventListener('submit', function(event) {        
        event.preventDefault();

        const form = event.target;
        var subject = document.getElementById('subject').value;
        var class_code = document.getElementById('class_code').value;
        var date_week = document.getElementById('date_week').value;
        var Period_from = document.getElementById('Period_from').value;
        var Period_to = document.getElementById('Period_to').value;
        var Date_start = document.getElementById('Date_start').value;
        var Date_end = document.getElementById('Date_end').value;
        var Learning_facility = document.getElementById('Learning_facility').value;
        var Room = document.getElementById('Room').value;
        var Teacher = document.getElementById('Teacher').value;
        var Team = document.getElementById('Team').value;
        var Code_online = document.getElementById('Code_online').value;
        var Learning_software = document.getElementById('Learning_software').value;
        var admin_code = document.getElementById('admin_code').value;
        const type_class = getSelectedRadioValue();
        var error = document.getElementById('error_notify_new_data');

        if (subject.trim() == '') {
            error.textContent = 'Vui lòng nhập tên môn học!';
            return;
        }
        if (Period_from.trim() == '') {
            error.textContent = 'Vui lòng chọn tiết bắt đầu!';
            return;
        }
        if (Period_to.trim() == '') {
            error.textContent = 'Vui lòng chọn tiết kết thúc!';
            return;
        }
        if (Date_start.trim() == '') {
            error.textContent = 'Vui lòng chọn ngày bắt đầu học!';
            return;
        }
        if (Date_end.trim() == '') {
            error.textContent = 'Vui lòng chọn ngày kết thúc học!';
            return;
        }
        if (class_code.trim() == '') {
            error.textContent = 'Vui lòng nhập mã lớp học!';
            return;
        }
        if (date_week.trim() == '') {
            error.textContent = 'Vui lòng chọn thứ trong tuần!';
            return;
        }


        if (Learning_facility.trim() == '') {
            error.textContent = 'Vui lòng chọn cơ sở học tập!';
            return;
        }
        if (Room.trim() == '') {
            error.textContent = 'Vui lòng nhập phòng học!';
            return;
        }
        if (Teacher.trim() == '') {
            error.textContent = 'Vui lòng nhập tên giảng viên!';
            return;
        }
        if (type_class == null) {
            error.textContent = 'Vui lòng chọn hình thức môn học!';
            return;
        }
        if (type_class === "TH") {
            if (Team.trim() == '') {
                error.textContent = 'Vui lòng nhập nhóm thực hành!';
                return;
            }

        } else if (type_class === "EX") {
            if (Team.trim() == '') {
                error.textContent = 'Vui lòng nhập nhóm thi!';
                return;
            }

        } else if (type_class === "ON") {
            if (Code_online.trim() == '') {
                error.textContent = 'Vui lòng nhập mã phòng!';
                return;
            }
            if (Learning_software.trim() == '') {
                error.textContent = 'Vui lòng nhập tên ứng dụng học online!';
                return;
            }
        }
        if (admin_code.trim() == '') {
            error.textContent = 'Vui lòng nhập mã admin!';
            return;
        }
        const admin_code_Regex = 20153;    
        if (admin_code != admin_code_Regex) {
            error.textContent = 'Sai mã Admin, vui lòng nhập lại!';
            return;
        }

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/add-new-data', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if(response.status == "success"){
                    error.textContent = response.message;
                    form.reset();
                } else {
                    error.textContent = response.message;
                }
            }
        };
        xhr.open('POST', form.action);
        xhr.send(formData);
    });
});





