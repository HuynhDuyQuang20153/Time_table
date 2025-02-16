// "refesh" - Nút refresh có data-refresh-button
document.querySelectorAll('[data-refresh-button]').forEach(button => {
    button.addEventListener('click', function () {
        location.reload(true); // Thực hiện reload bỏ qua cache
    });
});


// Gọi API để trả về danh sách các môn học
get_subject_name()

function get_subject_name() {
    fetch('/get-data')
    .then(response => response.json())
    .then(result => {
        var data = result.data;
        const subjectSelect = document.getElementById('subject');
        subjectSelect.innerHTML = `<option value="undefine">Chọn môn học</option>`; 
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.subject_name;
            option.textContent = item.subject_name;
            option.setAttribute('data-subject-id', item.id_subject);
            option.setAttribute('data-class-id', item.id_class);
            option.setAttribute('data-teacher-id', item.id_teacher);
            option.setAttribute('data-schedule-id', item.id_schedule);
            subjectSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching subjects:', error));    
}



    var delete_infor_form = document.getElementById('delete_info_from');
    if(delete_infor_form){
        delete_infor_form.addEventListener('click', function(event) {
            document.getElementById('error_notify_edit_data').textContent = '';
            updateFormFields(null);
        });
    } else {
        console.log("Không có phần tử id=delete_info_from ");
    }




    var show_popup = document.getElementById('show_popup_delete');
    if(show_popup){
        show_popup.addEventListener('click', function(event) {
            var popup = document.getElementById('popup-confirm-delete');
            popup.classList.add('active');
        });
    } else {
        console.log("Không có phần tử id=show_popup_delete ");
    }
    
    var close_popup = document.getElementById('btn_close_confirm');
    if(close_popup){
        close_popup.addEventListener('click', function(event) {
            var popup = document.getElementById('popup-confirm-delete');
            popup.classList.remove('active');
        });
    } else {
        console.log("Không có phần tử id=btn_close_confirm ");
    }
    
    
    function delete_all_data_json() {
        fetch('/delete-db')
        .then(response => response.json())
        .then(result => {
            var error = document.getElementById('error_notify_edit_data');
            if(result.status = "success"){
                error.textContent = result.message;
                var popup = document.getElementById('popup-confirm-delete');
                popup.classList.remove('active');
                get_subject_name();
                updateFormFields(null);

            } else {
                error.textContent = result.message;
            }
        })
        .catch(error => console.error('Error fetching subjects:', error));
    }
    

    function updateFormFields(result){
        if (!result || result.length === 0) {
            document.getElementById('Period_from').value = '';
            document.getElementById('Period_to').value = '';
            document.getElementById('Date_start').value = '';
            document.getElementById('Date_end').value = '';
            document.getElementById('subject').value = 'undefine';
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
            console.log(result.data[0]);
            
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





    document.getElementById('subject').addEventListener('change', function() {
        const selectedOption = this.selectedOptions[0]; // Lấy option đang chọn
        const schedule_id = selectedOption.getAttribute('data-schedule-id'); 
        document.getElementById('subject_id').value = selectedOption.getAttribute('data-subject-id'); 
        document.getElementById('class_id').value = selectedOption.getAttribute('data-class-id'); 
        document.getElementById('teacher_id').value = selectedOption.getAttribute('data-teacher-id'); 
        document.getElementById('schedule_id').value = schedule_id; 

        if (schedule_id) {
            // Gọi API để lấy chi tiết môn học
            fetch(`/get-data-details?schedule_id=${schedule_id}`)
                .then(response => response.json())
                .then(result => {    
                    updateFormFields(result)
                })
                .catch(error => console.error('Error fetching subject details:', error));

        } else {
            updateFormFields(null)
        }
    });
    






    function getSelectedRadioValue() {
        const radios = document.querySelectorAll('input[name="type_class"]');
        for (const radio of radios) {
            if (radio.checked) {
                return radio.value; 
            }
        }
        return null; 
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        const check_value_form = document.getElementById("submit_form_edit_data");
        check_value_form.addEventListener('submit', function(event) {        
            event.preventDefault();
    
            const form = event.target;
            var id_subject = document.getElementById('subject').value;
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
            var error = document.getElementById('error_notify_edit_data');
    
            if (id_subject.trim() == '') {
                error.textContent = 'Vui lòng nhập chọn môn học!';
                return;
            }
            if (class_code.trim() == '') {
                error.textContent = 'Vui lòng nhập mã học phần!';
                return;
            }
            if (date_week.trim() == '') {
                error.textContent = 'Vui lòng chọn thứ trong tuần!';
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
            if (admin_code.trim() == '') {
                error.textContent = 'Vui lòng nhập mã admin!';
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
    
            const admin_code_Regex = 20153;    
            if (admin_code != admin_code_Regex) {
                error.textContent = 'Sai mã Admin, vui lòng nhập lại!';
                return;
            }
    
            
            
            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/change-data', true);
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
            xhr.send(formData);
        });
    });