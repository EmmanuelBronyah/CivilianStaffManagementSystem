import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function AbsencesData(props) {
  const [absencesData, setAbsencesData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAbsencesData = async () => {
      try {
        const res = await api.get(`api/absences/${serviceId}/employee/`);
        setAbsencesData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchAbsencesData();
  }, []);

  const data = absencesData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/absences/edit/${data.id}`)
        }
      >
        <td title={data.absence}>{data.absence}</td>
        <td title={data.start_date}>{data.start_date}</td>
        <td title={data.end_date}>{data.end_date}</td>
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
