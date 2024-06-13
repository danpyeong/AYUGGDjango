import { ContainerDiv, CustomTextarea, ButtonsDiv, CountrySelect, SearchButton, ResultDiv, BlankDiv } from "./multiStyle/multiPageStyle";
import Nav from "../../nav/nav";
import { useState, useEffect } from 'react';
import Filter from './dataHandling/textareaFilter';
import AddBox from './addBox';

{/* <gameName> #<tagLine> (바위 게) 님이 로비에 참가하셨습니다. */}

function Multi() {
  const [inputText, setInputText] = useState('');
  const [filterTextList, setFilterTextList] = useState([]);
  const [finalDataList, setFinalDataList] = useState([]);

  //리스트화된 nickList 변경시 최종데이터에 넣음
  useEffect(() => {
    let dataList = [];
    filterTextList.map((data, index) => {
      fetch(`http://localhost:8000/search/${data[0]}/${data[1]}`)
      .then(response => response.json())
      .then(_data => {
        console.log(_data);
        if (_data.length === 0){
          alert('정확한 정보를 입력해주세요');
          return;
        } else {
          dataList[index] = _data;
        }
      }).then(() => {
        if (index === filterTextList.length -1) {
          setFinalDataList(dataList);
        }
      })
      .catch(() => {
        setTimeout(() => {
          alert('정확한 정보를 입력해주세요');
        }, 500);
      });
    });
  }, [filterTextList]);

  return (
    <div>
      <Nav />
      <BlankDiv />
      <ContainerDiv>
        <CustomTextarea
          id="textarea"
          placeholder="~~~~~ (바위 게) 님이 로비에 참가하셨습니다.
~~~~~ (돌거북) 님이 로비에 참가하셨습니다.
~~~~~ (어스름늑대) 님이 로비에 참가하셨습니다.
~~~~~ (칼날부리) 님이 로비에 참가하셨습니다.
~~~~~ (심술두꺼비) 님이 로비에 참가하셨습니다."
          value={inputText} onChange={(e) => { setInputText(e.target.value); }}
        />
        <BlankDiv />
        <BlankDiv />
        <ButtonsDiv>
          <CountrySelect>
            <option value="KR">KR</option>
            <option value="NA">NA</option>
          </CountrySelect>
          <SearchButton onClick={() => {
            setFilterTextList(Filter(inputText));
          }}>검색</SearchButton>
        </ButtonsDiv>
      </ContainerDiv>
      <BlankDiv />
      <ResultDiv>
        {
          finalDataList.map((data, index) => {
            console.log(finalDataList);
            return (<AddBox key={index} data={data} />);
          })
        }
      </ResultDiv>
    </div>
  );
}

export default Multi;
