import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function TerminationData(props) {
  const [terminationData, setTerminationData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTerminationData = async () => {
      try {
        const res = await api.get(
          `api/termination-of-appointment/${serviceId}/employee/`,
        );
        setTerminationData([res.data]);
        props.setLoading(false);
      } catch (error) {
        if (error.response.status === 404) {
          props.setLoading(false);
          return;
        }
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchTerminationData();
  }, []);

  const data = terminationData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/termination/edit/${data.id}`)
        }
      >
        <td title={data.cause_display}>{data.cause_display}</td>
        <td title={data.date}>{data.date}</td>
        <td title={data.authority}>{data.authority}</td>
        <td title={data.status_display}>{data.status_display}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
