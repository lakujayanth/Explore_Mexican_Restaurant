# **Embark on a global culinary journey within Mexico** 
## Exploring restaurants across three states: San Luis Potosi, Tamaulipas, and Morelos.

This restaurant recommender is an interactive application that empowers you to personalize your dining experience. With an intuitive interface, you can seamlessly navigate through a plethora of dining options across different states. The app provides a comprehensive set of filtering categories, including cuisines, ratings, price range, and parking options, allowing you to fine-tune your search according to your preferences.<br>

*Dive into a world of culinary possibilities as you explore and discover the perfect restaurant that aligns with your desired criteria, ensuring a tailored and delightful dining journey.*<br>

To experience the app live, visit: https://exploremexicanrestaurant-restaurant-mx.streamlit.app/ 

# Data Source<br>
The data for this project is sourced from the UC Irvine Machine Learning Repository, available at https://archive.ics.uci.edu/dataset/232/restaurant+consumer+data. The input data consists of three main entities: Restaurants, Consumers, and User-Item-Rating. These files collectively provide essential information about restaurants, customers, and the ratings users have given to various items, forming the foundation for our analysis and recommendation system. By leveraging this diverse dataset, we aim to extract valuable insights and enhance the user experience in discovering and selecting restaurants.

<ol>
  <li>Restaurants </li><em> This dataset includes information collected about various restaurants. Each of these datasets can be associated with a unique placeID.</em><br><br>

  <ol> 
  <li>chefmozaccepts.csv – Payment method (Card, Cash)</li>
  <li> chefmozcuisine.csv – Cuisine type</li>
  <li> chefmozhours4.csv - Work hours</li>
  <li> chefmozparking.csv - Parking type availability</li>	
  <li> geoplaces2.csv - Geographical presence </ol>
<br>
  <li>Consumers </li><em>This dataset encompasses information gathered about consumers. Each of these datasets can be linked to a unique userID.</em> <br><br>
  <ol> 
  <li>usercuisine.csv - Cuisine type</li>
  <li>userpayment.csv – payment method</li>
  <li>userprofile.csv – Consumers data </li></ol>	
  <br>
  <li>Restaurants - Consumers Rating</li><em>The Rating dataset includes the food, service, and overall ratings given by consumers to a restaurant. Each rating is uniquely identified by the combination of placeID and userID</em><br><br>
  <ol> 
  <li>rating_final.csv - Rating details</li></ol>
</ol>

# Future Enhancements: <br>
There are additional enhancements we can make to the existing recommendation App. By incorporating work hours data, which has already been cleaned as part of the code, we can introduce new features to facilitate a more detailed exploration of the restaurant list. This includes criteria such as the day of operation (workdays or weekends), operating hours (opening and closing times), and accepted methods of payment. Furthermore, we have the opportunity to expand the geographical coverage of the app by adding data for other states in Mexico, providing a broader and more comprehensive dining experience for users
