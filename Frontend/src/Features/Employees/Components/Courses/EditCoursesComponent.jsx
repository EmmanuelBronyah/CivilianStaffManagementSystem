import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import CoursesInputBoxes from "./CoursesInputBoxesComponent";
import api from "../../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdDelete } from "react-icons/md";
import askToDelete from "../../../../utils/askToDelete";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function EditCourses() {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});
  const [loadingData, setLoadingData] = useState(true);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { serviceId, courseId } = useParams();

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const res = await api.get(`api/courses/${courseId}/detail/`);
        setInitialData({
          courseType: res.data.course_type,
          place: res.data.place,
          dateCommenced: res.data.date_commenced,
          dateEnded: res.data.date_ended,
          qualification: res.data.qualification,
          result: res.data.result,
          authority: res.data.authority,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
        setLoadingData(false);
      } catch (error) {
        if (error.response?.status === 404) {
          setResponse({
            message: "Course not found",
            type: "error",
            id: Date.now(),
          });
          navigate(`/home/employees/${serviceId}/courses`);
          return;
        }

        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchCourse();
  }, []);

  const updateCourse = async () => {
    setLoading(true);

    const payload = {
      course_type: formData.courseType,
      place: formData.place,
      date_commenced: formData.dateCommenced || null,
      date_ended: formData.dateEnded || null,
      qualification: formData.qualification,
      result: formData.result,
      authority: formData.authority,
    };

    try {
      const res = await api.patch(`api/courses/${courseId}/edit/`, payload);
      setFormData({
        courseType: res.data.course_type,
        place: res.data.place,
        dateCommenced: res.data.date_commenced,
        dateEnded: res.data.date_ended,
        qualification: res.data.qualification,
        result: res.data.result,
        authority: res.data.authority,
        createdAt: res.data.date_added,
        createdBy: res.data.created_by_display,
        updatedAt: res.data.date_modified,
        updatedBy: res.data.updated_by_display,
      });
      setResponse({
        message: "Course updated",
        id: Date.now(),
      });
      setLoading(false);
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      setLoading(false);
      return;
    }
  };

  const discardChanges = () => {
    const updatedInitialData = {
      ...initialData,
      createdAt: formData.createdAt,
      createdBy: formData.createdBy,
      updatedAt: formData.updatedAt,
      updatedBy: formData.updatedBy,
    };

    setFormData(updatedInitialData);
  };

  const initiateDeletion = async () => {
    const result = await askToDelete(theme);
    if (!result.isConfirmed) return;

    try {
      const res = await api.delete(`api/courses/${courseId}/delete/`);
      if (res.status === 204) {
        navigate(`/home/employees/${serviceId}/courses`);
      }
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loadingData ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button
              className={style.addOccurrence}
              onClick={() => navigate(`/home/employees/${serviceId}/courses`)}
            >
              All Courses
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <CoursesInputBoxes
          formData={formData}
          setFormData={setFormData}
          loadingData={loadingData}
        />
        <div className={style.editOccurrenceButtons}>
          <div className={style.emptyDiv}></div>
          <div className={style.updateCancelButtons}>
            {loadingData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button onClick={updateCourse}>
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save Changes"
                )}
              </button>
            )}
            {loadingData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button className={style.cancelButton} onClick={discardChanges}>
                Cancel
              </button>
            )}
          </div>
          {loadingData ? (
            <BaseSkeleton width={40} />
          ) : (
            <MdDelete className={style.trashIcon} onClick={initiateDeletion} />
          )}
        </div>
      </div>
    </div>
  );
}
