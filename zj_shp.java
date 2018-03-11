import org.gdal.osr.*;
import org.omg.CORBA.ExceptionList;
import org.gdal.ogr.*;
import org.gdal.gdal.*;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class zj_3 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		// 链接数据库
		// 声明Connection对象
		Connection con;
		// 驱动程序名
		String driver = "com.mysql.jdbc.Driver";
		// URL指向要访问的数据库名mydata
		String url = "jdbc:mysql://localhost:3306/testdb?useUnicode=true&characterEncoding=utf-8&useSSL=false";
		// MySQL配置时的用户名
		String user = "root";
		// MySQL配置时的密码
		String password = "xxxxxxxx";
		// 遍历查询结果集
		try {
			// 加载驱动程序
			Class.forName(driver);
			// 1.getConnection()方法，连接MySQL数据库！！
			con = DriverManager.getConnection(url, user, password);
			if (!con.isClosed())
				System.out.println("Succeeded connecting to the Database!");
			// 2.创建statement类对象，用来执行SQL语句！！
			Statement statement = con.createStatement();

			// 要执行的SQL语句
			String sql = "SELECT * FROM testdb.sh_area where id>933 and id<1036 and level=3;";//浙江区级编码
			// 3.ResultSet类，用来存放获取的结果集！！
			ResultSet rs = statement.executeQuery(sql);
			String strToVectorFile = "";
			strToVectorFile = "D:\\Work\\Test\\zjjwd.shp";
			// 注册所有的驱动
			ogr.RegisterAll();

			// 为了支持中文路径，请添加下面这句代码
			gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");
			// 为了使属性表字段支持中文，请添加下面这句
			gdal.SetConfigOption("SHAPE_ENCODING", "CP936");
			// 创建数据，这里以创建ESRI的shp文件为例
			String strDriverName = "ESRI Shapefile";
			org.gdal.ogr.Driver oDriver = ogr.GetDriverByName(strDriverName);
			if (oDriver == null) {
				System.out.println(" 驱动不可用！\n");
				return;
			}

			// 创建数据源
			DataSource oDS = oDriver.CreateDataSource(strToVectorFile, null);
			if (oDS == null) {
				System.out.println("创建矢量文件失败！\n");
				return;
			}

			// 创建图层
			Layer oLayer = oDS.CreateLayer("Test", null, ogr.wkbUnknown, null);
			if (oLayer == null) {
				System.out.println("图层创建失败！\n");
				return;
			}

			// 创建属性表
			// 先创建一个叫FieldID的整型属性
			FieldDefn oFieldID = new FieldDefn("ID", ogr.OFTInteger);
			oLayer.CreateField(oFieldID, 0);

			// 再创建一个叫FeatureName的字符型属性，字符长度为50
			FieldDefn oFieldName = new FieldDefn("Name", ogr.OFTString);
			oFieldName.SetWidth(100);
			oLayer.CreateField(oFieldName, 1);
			
			// 再创建一个叫FeatureName的字符型属性，字符长度为50
			FieldDefn oFieldshortName = new FieldDefn("shortName", ogr.OFTString);
			oFieldshortName.SetWidth(100);
			oLayer.CreateField(oFieldshortName,2 );
			
			// 再创建一个叫FeatureName的字符型属性，字符长度为50
			FieldDefn olng = new FieldDefn("lng", ogr.OFTString);
			oFieldName.SetWidth(100);
			oLayer.CreateField(olng, 3);
			// 再创建一个叫FeatureName的字符型属性，字符长度为50
			FieldDefn olat = new FieldDefn("lat", ogr.OFTString);
			oFieldName.SetWidth(100);
			oLayer.CreateField(olat, 4);

			FeatureDefn oDefn = oLayer.GetLayerDefn();
			int id = 0;
			String name = null;
			String shortname = null;
			String lng = null;// 经度
			String lat = null;// 纬度
			while (rs.next()) {
				// 获取数据
				id = rs.getInt("id");
				name = rs.getString("name");
				shortname=rs.getString("shortname");
				lng = rs.getString("lng");
				lat = rs.getString("lat");
				// 根据数据创建要素
				Feature oFeature = new Feature(oDefn);
				oFeature.SetField(0, id);
				oFeature.SetField(1, name);
				oFeature.SetField(2, shortname);
				oFeature.SetField(3, lng);
				oFeature.SetField(4, lat);
				Geometry geom = Geometry.CreateFromWkt("Point(" + Double.valueOf(lng) + " " + Double.valueOf(lat) + ")");//根据经纬度设定空间位置
				oFeature.SetGeometry(geom);

				oLayer.CreateFeature(oFeature);
				System.out.println(oLayer.GetFeatureCount());
				// 输出结果
				System.out.println("\t name: " + name + "\t shortname: " + shortname +"\t 经度: " + lng + "\t 纬度: " + lat);
			}
			oDS.SyncToDisk();

		} catch (

		ClassNotFoundException e) {
			// 数据库驱动类异常处理
			System.out.println("Sorry,can`t find the Driver!");
			e.printStackTrace();
		} catch (SQLException e) {
			// 数据库连接失败异常处理
			e.printStackTrace();
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		} finally {
			System.out.println("数据库数据成功获取！！");
		}
	}
}
