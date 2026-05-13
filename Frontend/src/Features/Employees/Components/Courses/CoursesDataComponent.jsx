import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function CoursesData(props) {
  const [coursesData, setCoursesData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCoursesData = async () => {
      try {
        const res = await api.get(`api/courses/${serviceId}/employee/`);
        setCoursesData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchCoursesData();
  }, []);

  const data = coursesData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/courses/edit/${data.id}`)
        }
      >
        <td title={serviceId}>{serviceId}</td>
        <td title={data.course_type}>{data.course_type}</td>
        <td title={data.place}>{data.place}</td>
        <td title={data.date_commenced}>{data.date_commenced}</td>
        <td title={data.date_ended}>{data.date_ended}</td>
        <td title={data.qualification}>{data.qualification}</td>
        <td title={data.result}>{data.result}</td>
        <td title={data.authority}>{data.authority}</td>
        <td title={data.date_added}>{data.date_added}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
