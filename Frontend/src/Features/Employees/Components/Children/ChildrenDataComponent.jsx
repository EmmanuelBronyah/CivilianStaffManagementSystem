import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function ChildrenData(props) {
  const [childrenData, setChildrenData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChildrenData = async () => {
      try {
        const res = await api.get(`api/children/${serviceId}/employee/`);
        setChildrenData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchChildrenData();
  }, []);

  const data = childrenData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/children/edit/${data.id}`)
        }
      >
        <td title={data.child_name}>{data.child_name}</td>
        <td title={data.dob}>{data.dob}</td>
        <td title={data.gender_display}>{data.gender_display}</td>
        <td title={data.other_parent}>{data.other_parent}</td>
        <td title={data.authority}>{data.authority}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
