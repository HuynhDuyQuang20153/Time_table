# python app.py     (để chạy chương trình)
# npm run obfuscate (để làm rối mã js)

from flask import Flask, request, render_template, jsonify
from flask_sse import sse
import os
import logging

# Module nội bộ
from extensions import db, migrate
from sqlalchemy import create_engine, inspect
from Request_processing import (
    processing_delete_data, processing_get_data, 
    processing_edit_data, processing_insert_data
)


app = Flask(__name__)

BASE_FOLDER = "Database"
os.makedirs(BASE_FOLDER, exist_ok=True)
DATABASE_PATH = os.path.join(os.getcwd(), BASE_FOLDER, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(sse, url_prefix="/stream")


log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'error.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


with app.app_context():
    try:
        connection = db.engine.connect()
        print("Kết nối cơ sở dữ liệu thành công!")
        engine = create_engine('sqlite:///Database/app.db')  
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Các bảng trong cơ sở dữ liệu:", tables)
        connection.close()

    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        logging.error("Error occurred", exc_info=True)




# ----------------RENDER HTML ------------------ #
@app.route('/next-week')
def next_week():
    try:    
        week_offset = request.args.get('week_offset', '0')  # Giá trị mặc định là '0' nếu không có tham số 
        try:
            week_offset = int(week_offset)
        except ValueError:
            week_offset = 0  # Nếu giá trị không hợp lệ, sử dụng tuần hiện tại  

        return processing_get_data.get_time_table(week_offset)
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at next_week(): {e}")
        logging.error("Error occurred at next_week()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại next_week()!'}), 500
    
    


# ---------------- TRANG CHỦ ------------------ #
@app.route('/', endpoint='index')
def index():
    try:        
        return render_template('index.html')
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at index(): {e}")
        logging.error("Error occurred at index()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại index()!'}), 500




# ---------------- TRANG THÊM LỊCH HỌC ------------------ #
@app.route('/new_timetable')
def new_data_page():
    try:        
        return render_template('new_timetable.html')
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at new_data_page(): {e}")
        logging.error("Error occurred at new_data_page()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại new_data_page()!'}), 500




# ---------------- TRANG EDIT LỊCH HỌC ------------------ #
@app.route('/edit_timetable')
def edit_timetable_page():
    try:       
        facilities = processing_get_data.get_facilities()
        return render_template('edit_timetable.html', facilities=facilities)
        # return render_template('edit_timetable.html')
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at edit_timetable_page(): {e}")
        logging.error("Error occurred at edit_timetable_page()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại edit_timetable_page()!'}), 500




# ----------------LẤY TÊN MÔN HỌC TẠI EDIT FORM ------------------ #
@app.route('/get-data')
def get_subject_name():
    try:    
        return processing_get_data.get_subject_name()
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at get_subject_name(): {e}")
        logging.error("Error occurred at get_subject_name()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại get_subject_name()!'}), 500
    



# ---------------- XÓA DATABASE ------------------ #
@app.route('/delete-db')
def get_delete_data():
    try:    
        return processing_delete_data.delete_db()
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at get_delete_data(): {e}")
        logging.error("Error occurred at get_delete_data()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại get_delete_data()!'}), 500
    
   


# ---------------- LẤY THÔNG TIN CHI TIẾT MÔN HỌC TẠI EDIT FORM ------------------ #
@app.route('/get-data-details', methods=['GET'])
def get_data_details():
    try:    
        id_subject = request.args.get('id_subject', None)  
        try:
            id_subject = int(id_subject)
        except ValueError:
            id_subject = None   

        return processing_get_data.get_data_details(id_subject)
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at get_data_details(): {e}")
        logging.error("Error occurred at get_data_details()", exc_info=True)
        return jsonify({'error': 'Đã xảy ra lỗi khi tại get_data_details()!'}), 500
 



@app.route('/add-new-data', methods=['POST'])
def add_new_data():    
    try:
        data = request.form.to_dict()
        return processing_insert_data.add_data(data)
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at save_data(): {e}")
        logging.error("Error occurred at save_data()", exc_info=True)
        return jsonify({"message": 'Đã xảy ra lỗi khi tại save_data()!' + str(e), "status": "error"}), 500
    
    


@app.route('/change-data', methods=['POST'])
def save_data():
    try:
        data = request.form.to_dict()
        return processing_edit_data.change_data(data)
    
    except Exception as e:
        db.session.rollback()  
        print(f"Error occurred at save_data(): {e}")
        logging.error("Error occurred at save_data()", exc_info=True)
        return jsonify({"message": 'Đã xảy ra lỗi khi tại save_data()!' + str(e), "status": "error"}), 500



if __name__ == '__main__':
    app.run(debug=True)