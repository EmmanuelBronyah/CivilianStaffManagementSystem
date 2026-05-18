import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function IdentityData(props) {
  const [identityData, setIdentityData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchIdentityData = async () => {
      try {
        const res = await api.get(`api/identity/${serviceId}/detail/`);
        setIdentityData([res.data]);
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
    fetchIdentityData();
  }, []);

  const data = identityData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/identity/edit/${data.id}`)
        }
      >
        <td title={data.voters_id}>{data.voters_id}</td>
        <td title={data.national_id}>{data.national_id}</td>
        <td title={data.glico_id}>{data.glico_id}</td>
        <td title={data.nhis_id}>{data.nhis_id}</td>
        <td title={data.tin_number}>{data.tin_number}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
