// "refesh" - Nút refresh có data-refresh-button
document.querySelectorAll('[data-refresh-button]').forEach(button => {
    button.addEventListener('click', function () {
        location.reload(true); // Thực hiện reload bỏ qua cache
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const weekDays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
    let offset = 0;

    function get_Date_Start_Of_Week() {
        const today = new Date();
        const day = today.getDay();
        const diff = today.getDate() - day + (day === 0 ? -6 : 1); // Nếu Chủ Nhật, tính từ Thứ Hai
        return new Date(today.setDate(diff));
    }

    let current_Week_Start = get_Date_Start_Of_Week();
    let displayed_Week = new Date(current_Week_Start);

    update_Week(displayed_Week, offset);

    document.getElementById('next_week').addEventListener('click', () => changeWeek(7));
    document.getElementById('last_week').addEventListener('click', () => changeWeek(-7));
    document.getElementById('current_week').addEventListener('click', () => resetWeek());

    function changeWeek(days) {
        displayed_Week.setDate(displayed_Week.getDate() + days);
        offset += days / 7;
        console.log(offset);
        update_Week(displayed_Week, offset);
    }

    function resetWeek() {
        displayed_Week = new Date(current_Week_Start);
        offset = 0;
        update_Week(displayed_Week, 0);
    }

    function update_Week(startOfWeek, weekOffset) {
        const weekDates = getWeekDates(startOfWeek);
        weekDays.forEach((id, index) => {
            document.getElementById(id).innerHTML = `Thứ ${["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy", "Chủ Nhật"][index]} <br> ${weekDates[index]}`;
        });

        fetch(`/next-week?week_offset=${weekOffset}`)
            .then(response => response.json())
            .then(result => {
                renderSchedule(result);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function renderSchedule(result) {
        const scheduleBody = document.getElementById('schedule_body');
        scheduleBody.innerHTML = '';

        document.getElementById('calender').innerHTML =
            `Tuần: ${formatDate(new Date(result.week_start))} - ${formatDate(new Date(result.week_end))}`;

        const periods = ["Sáng", "Chiều", "Tối"];
        periods.forEach((period, index) => {
            let row = document.createElement('tr');
            row.innerHTML = `<td>${period}</td>`;

            for (let day = 1; day <= 7; day++) {
                let cell = document.createElement('td');
                result.filtered_items.forEach(item => {
                    if (isItemInPeriod(item, index, day)) {
                        cell.appendChild(createScheduleBox(item));
                    }
                });
                row.appendChild(cell);
            }
            scheduleBody.appendChild(row);
        });
    }

    function isItemInPeriod(item, periodIndex, day) {
        const period_ranges = [[1, 6], [7, 12], [13, 15]];
        return (
            period_ranges[periodIndex][0] <= item.period_from &&
            item.period_from <= period_ranges[periodIndex][1] &&
            item.date_week === day
        );
    }

    function createScheduleBox(item) {
        const classTypes = { "LT": "theory", "TH": "practice", "ON": "online", "EX": "exam" };
        let div = document.createElement('div');
        div.className = `box_info ${classTypes[item.type_class] || ""}`;
        div.innerHTML = `
            ${item.suspension_status === "TN" ? `<div class="tam_ngung"><span>Tạm ngưng</span></div>` : ""}
            <div class="name_object">${item.subject_name}</div>
            <div>${item.class_code}</div>
            <div>Tiết: ${item.period_from} - ${item.period_to}</div>
            <div>Phòng: ${item.room}</div>
            <div>GV: ${item.teacher_name}</div>
            <div>Cơ sở: ${item.learning_facility}</div>
            <div>Nhóm: ${item.team}</div>
            ${item.type_class === "ON" ? `
                <div>Code: ${item.code_online}</div>
                <div>Phần mềm: ${item.learning_software}</div>` : ""}
        `;
        return div;
    }

    function getWeekDates(startOfWeek) {
        return Array.from({ length: 7 }, (_, i) => formatDate(new Date(startOfWeek.getTime() + i * 86400000)));
    }

    function formatDate(date) {
        return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()}`;
    }
});





