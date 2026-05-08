import Clock from './Clock';
import SensorCard from './SensorCard';
import SwitchStateCard from './SwitchStateCard';

function StatusBar() {
    return (
        <section id="center-stretch">

          <div className="left">
            <SensorCard name="Temperature" reading="20.5C" high="22.0C" avg="19.8C" low="18.5C" color="#9e743d"/>
            <SensorCard name="Humidity" reading="50%" high="60%" avg="45%" low="30%" color="#21deff"/>

            <SwitchStateCard name="Ventilation" reading="ON" uptime="3" avgUptime="2" downtime="5" color="#c472fb"/>
            <SwitchStateCard name="fan" reading="OFF" uptime="3" avgUptime="2" downtime="5" color="#96ff54"/>

            {/* <SensorCard name="Sunlight" reading="2" high="3" avg="2" low="1" color="yellow"/> } */}
            {/* <SensorCard name="Moisture" reading="2" high="3" avg="2" low="1" color="blue"/> */}
            {/* <SensorCard name="Water" reading="6.5" high="7.0" avg="6.8" low="6.5" color="blue"/> */}
            
          </div>

          <div className="center">
            
          </div>

          <div className="right">
            <Clock /> 
          </div>

        </section>
    );
}

export default StatusBar;