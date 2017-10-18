import edu.sxu.cs.database.*;
import org.apache.ibatis.session.SqlSession;
import org.junit.Test;

import java.util.Date;

public class DBTest {
    @Test
    public void test() {
        UserNumber number = new UserNumber();
        number.setId("1");
        number.setTime(new Date());
        number.setNumber(11);
        SqlSession session = MySession.getSession().openSession();
        session.getMapper(UserNumberOperation.class).add(number);
        session.commit();
    }
    @Test
    public void test2(){
        UserRate rate = new UserRate();
        rate.setId("1");
        rate.setTime(new Date());
        rate.setRate(0.4444f);
        SqlSession session=MySession.getSession().openSession();
        session.getMapper(UserRateOperation.class).add(rate);
        session.commit();
    }
}
