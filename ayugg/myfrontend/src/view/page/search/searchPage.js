import { useEffect,useState } from "react";
import { useDispatch } from 'react-redux';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import Nav from "../../nav";
import TopBox from "./boxes/topBox";
import { BlankDiv, ContainerDiv } from "./searchStyle/topBoxStyle";
import Button from "./boxes/refreshButton"
import BottomBox from "./boxes/bottomBox";
import { fetchDataRequest, fetchDataSuccess, fetchDataFailure } from "../../../redux/dataSlice";

function SearchPage() {
  const dispatch = useDispatch();
  let location = useLocation();
  let navigate = useNavigate();
  const { gameName, tagLine } = useParams();

  const [data, setData] = useState(null);

  useEffect(() => {
    // const nickname = location.state.nickname;
    dispatch(fetchDataRequest());

    fetch(`http://localhost:8000/search/${gameName}/${tagLine}`)
      .then(response => response.json())
      .then(data => {
        if (data.length === 0){
          dispatch(fetchDataFailure(error));
          navigate('/');
          setTimeout(() => {
            alert('정확한 소환사 이름을 입력해주세요');
          }, 500);
          return;
        } else {
          dispatch(fetchDataSuccess(data));
          setData(data);
        }
      })
      .catch(error => {
        dispatch(fetchDataFailure(error));
        navigate('/');
        setTimeout(() => {
          alert('정확한 소환사 이름을 입력해주세요');
        }, 500);
      });
  }, [dispatch, navigate]);

  return (
    <div>
      <Nav></Nav>
      {data &&(
        <ContainerDiv>
          <TopBox />
          <Button />
          <BlankDiv />
          <BottomBox />
        </ContainerDiv>
      )}
      <BlankDiv />
    </div>
  );
}

export default SearchPage;