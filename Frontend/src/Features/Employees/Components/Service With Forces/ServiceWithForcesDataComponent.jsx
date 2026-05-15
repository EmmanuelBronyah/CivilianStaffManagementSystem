import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function ServiceWithForcesData(props) {
  const [serviceWithForcesData, setServiceWithForcesData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchServiceWithForcesData = async () => {
      try {
        const res = await api.get(
          `api/service-with-forces/${serviceId}/employee/`,
        );
        setServiceWithForcesData(res.data);
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
    fetchServiceWithForcesData();
  }, []);

  const data = serviceWithForcesData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(
            `/home/employees/${serviceId}/serviceWithForces/edit/${data.id}`,
          )
        }
      >
        <td title={data.service_date}>{data.service_date}</td>
        <td title={data.last_unit_display}>{data.last_unit_display}</td>
        <td title={data.service_id}>{data.service_id}</td>
        <td title={data.military_rank_display}>{data.military_rank_display}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
