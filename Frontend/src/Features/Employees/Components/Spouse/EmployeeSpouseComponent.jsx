import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeSpouse() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}
