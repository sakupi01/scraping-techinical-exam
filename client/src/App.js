import { BrowserRouter, Routes, Route} from 'react-router-dom';
import {Venues} from './Venues';
import Search from './Search';

function App() {
  return (
    <div>
      <BrowserRouter>
            <Routes>
              <Route exact path='/' 
              element={<Search />}
              />
              <Route exact path='/result' 
              element={<Venues />}
              />
            </Routes>
      </BrowserRouter>

    </div>
  );
}

export default App;
