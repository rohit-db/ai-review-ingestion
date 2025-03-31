# Databricks notebook source
# MAGIC %run ./00_CONFIG

# COMMAND ----------

SCHEMA 

# COMMAND ----------

from auto_topic.domains import DomainConfigTable, Domain

# COMMAND ----------

dct = DomainConfigTable(catalog=CATALOG, schema=SCHEMA, table=QUESTIONS_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Define Domains
# MAGIC
# MAGIC **Define different domains and questions you want answered. You can have a lot of these and the llm will do a two pass, first identify the topic and then map to fill out all the information that needs to be filled out in the domain**
# MAGIC
# MAGIC Each domain will require:
# MAGIC 1. topic -> 1 word all lower case
# MAGIC 2. when ->  topic condition: succinct sentence aligning topic name with specific entities aligning with this topic, e.g. in retail topic name defect may align with sneaker but in manufacturing topic name 
# MAGIC 3. details -> single sentence expression what you want extracted (just additional info)
# MAGIC
# MAGIC You can optionally extract additional info in each topic using the `.with_additional_info` with the following two fields:
# MAGIC 1. item_name -> which is only alpha numeric json key for labeling the concept/question
# MAGIC 2. item_description -> the details in how to extract the item/concept/detail
# MAGIC
# MAGIC For example when someone is describing a review and if they describe the item was used as a gift you may want to extract that detail if you think this may be something that you can use to suggest specific items as great gifts during a specific season.
# MAGIC

# COMMAND ----------

# dct.with_topic(
#   topic=Domain(
#     topic="product",
#     when="generally when the user is referering to the product they have purchased",
#     details="<summary of the review regarding the product>"
#   ).with_additional_info(
#     item_name="can_be_used_as_gift",
#     item_description="the product was used as a gift or will be used as a gift <yes/no/unsure>"
#   ).with_additional_info(
#     item_name="as_advertized",
#     item_description="the product behaved as advertized whether it be description or other reviews <yes/no/unsure>"
#   )
# )

# dct.with_topic(
#   topic=Domain(
#     topic="defects",
#     when="generally when the user is referering to the product they have purchased",
#     details="<summary of the review regarding the product>",
#   ).with_additional_info(
#     item_name="defect_level",
#     item_description="the level of defectiveness to the product use your best judgement <small/medium/large>"
#   ).with_additional_info(
#     item_name="misinformation",
#     item_description="the product does not work as described <yes/no>"
#   )
# )


# dct.with_topic(
#   topic=Domain(
#     topic="delivery",
#     when="generally when the user is referering to the product they have purchased",
#     details="<summary of the review regarding the product>",
#   ).with_additional_info(
#     item_name="defect_level",
#     item_description="the level of defectiveness to the product use your best judgement <small/medium/large>"
#   ).with_additional_info(
#     item_name="misinformation",
#     item_description="the product does not work as described <yes/no>"
#   )
# )

# dct.with_topic(
#   topic=Domain(
#     topic="movies",
#     when="generally when the user is referering to the movies they have purchased",
#     details="<summary of the review regarding the product>",
#   ).with_additional_info(
#     item_name="enjoyment",
#     item_description="the level of enjoyment to the moview use your best judgement <1-5>"
#   ).with_additional_info(
#     item_name="genre",
#     item_description="the genre of the movie"
#   ).with_additional_info(
#     item_name="audio_issues",
#     item_description="were there audio quality issues <yes/no>"
#   ).with_additional_info(
#     item_name="video_quality_issues",
#     item_description="were there video quality issues <yes/no>"
#   )
# )


# COMMAND ----------

# DBTITLE 1,Costa Coffee
dct.with_topic(
  topic=Domain(
    topic="customer_service",
    when="Generally when the user is referring to the service they received from the staff.",
    details="Summary of the review regarding the quality of service provided by the staff.",
  ).with_additional_info(
    item_name="staff_friendliness",
    item_description="How friendly was the staff? <yes/no/unsure>"
  ).with_additional_info(
    item_name="service_speed",
    item_description="The speed of service <fast/slow/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="coffee_quality",
    when="When the user is commenting on the taste, temperature, or preparation of the coffee.",
    details="Summary of the review regarding the quality of the coffee.",
  ).with_additional_info(
    item_name="temperature",
    item_description="Was the coffee served at the correct temperature? <yes/no/unsure>"
  ).with_additional_info(
    item_name="flavor_intensity",
    item_description="The intensity of the coffee flavor <strong/weak/average>"
  ).with_additional_info(
    item_name="consistency",
    item_description="Consistency of coffee quality across visits <consistent/inconsistent>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="food_quality",
    when="When the user is referring to the quality of food items like snacks, sandwiches, or pastries.",
    details="Summary of the review regarding the quality of the food.",
  ).with_additional_info(
    item_name="freshness",
    item_description="Freshness of the food <fresh/stale/unsure>"
  ).with_additional_info(
    item_name="portion_size",
    item_description="Adequacy of the portion size <adequate/insufficient/excessive>"
  ).with_additional_info(
    item_name="taste",
    item_description="Overall taste of the food <delicious/bland/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="ambiance",
    when="When the user is discussing the environment, decor, or atmosphere of the location.",
    details="Summary of the review regarding the ambiance of the cafe.",
  ).with_additional_info(
    item_name="cleanliness",
    item_description="The cleanliness of the location <clean/dirty/average>"
  ).with_additional_info(
    item_name="noise_level",
    item_description="The noise level in the cafe <quiet/noisy/average>"
  ).with_additional_info(
    item_name="lighting",
    item_description="Appropriateness of lighting <well-lit/dim/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="hygiene_and_cleanliness",
    when="When the user is mentioning cleanliness, particularly in seating areas, restrooms, or overall hygiene.",
    details="Summary of the review regarding the cleanliness and hygiene standards.",
  ).with_additional_info(
    item_name="restroom_cleanliness",
    item_description="Cleanliness of the restroom <clean/dirty/unusable>"
  ).with_additional_info(
    item_name="table_cleanliness",
    item_description="Cleanliness of the tables and seating area <clean/dirty/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="seating_and_space",
    when="When the user refers to the seating arrangement, space, or comfort level.",
    details="Summary of the review regarding the seating and space available.",
  ).with_additional_info(
    item_name="comfort",
    item_description="Comfort level of the seating <comfortable/uncomfortable/average>"
  ).with_additional_info(
    item_name="availability",
    item_description="Availability of seating during the visit <plenty/limited/none>"
  ).with_additional_info(
    item_name="layout",
    item_description="Effectiveness of the seating layout <spacious/cramped/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="wifi_and_connectivity",
    when="When the user discusses the availability and quality of Wi-Fi or mobile reception.",
    details="Summary of the review regarding Wi-Fi and connectivity.",
  ).with_additional_info(
    item_name="wifi_quality",
    item_description="Quality of the Wi-Fi connection <strong/weak/unavailable>"
  ).with_additional_info(
    item_name="mobile_reception",
    item_description="Mobile network reception quality <strong/weak/unavailable>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="queue_management_and_speed",
    when="When the user comments on the efficiency of queue management or speed of service.",
    details="Summary of the review regarding how well queues were managed and the speed of service.",
  ).with_additional_info(
    item_name="queue_time",
    item_description="Time spent in the queue <short/long/average>"
  ).with_additional_info(
    item_name="service_efficiency",
    item_description="Efficiency of service <efficient/inefficient/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="staff_attitude_and_behavior",
    when="When the user provides feedback on the attitude and behavior of staff members.",
    details="Summary of the review regarding staff behavior.",
  ).with_additional_info(
    item_name="politeness",
    item_description="Was the staff polite and courteous? <yes/no/unsure>"
  ).with_additional_info(
    item_name="helpfulness",
    item_description="Was the staff helpful? <helpful/unhelpful/average>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="special_promotions_and_offers",
    when="When the user mentions any promotions or special offers available at the location.",
    details="Summary of the review regarding the effectiveness or appeal of promotions.",
  ).with_additional_info(
    item_name="promotion_effectiveness",
    item_description="How effective was the promotion in attracting customers? <effective/ineffective/neutral>"
  ).with_additional_info(
    item_name="offer_clarity",
    item_description="Clarity of the terms and conditions of the promotion <clear/confusing/unclear>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="out_of_stock_items",
    when="When the user comments on items that were unavailable or out-of-stock.",
    details="Summary of the review regarding the availability of products.",
  ).with_additional_info(
    item_name="item_availability",
    item_description="Availability of the desired items <available/unavailable/unsure>"
  ).with_additional_info(
    item_name="frequency",
    item_description="Frequency of encountering out-of-stock items <rare/common/always>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="customer_satisfaction",
    when="When the user provides general feedback on their satisfaction with the overall experience.",
    details="Summary of the review regarding overall customer satisfaction.",
  ).with_additional_info(
    item_name="overall_experience",
    item_description="Overall customer experience <positive/negative/mixed>"
  ).with_additional_info(
    item_name="likelihood_to_return",
    item_description="Likelihood of returning to the location <high/low/unsure>"
  )
)

dct.with_topic(
  topic=Domain(
    topic="health_and_safety",
    when="When the user raises any health or safety concerns during their visit.",
    details="Summary of the review regarding any health or safety issues.",
  ).with_additional_info(
    item_name="health_issues",
    item_description="Any health issues encountered <yes/no>"
  ).with_additional_info(
    item_name="safety_concerns",
    item_description="Any safety concerns raised <yes/no>"
  )
)


# COMMAND ----------

# DBTITLE 1,KFC
# CORE FOOD QUALITY
dct.with_topic(
  topic=Domain(
    topic="chicken_quality",
    when="Mentions of fried chicken taste, texture, or preparation.",
    details="Evaluation of chicken preparation and taste characteristics.",
  ).with_additional_info(
    item_name="crispiness",
    item_description="Crispiness level of fried chicken <crispy/soggy/chewy>"
  ).with_additional_info(
    item_name="seasoning",
    item_description="Flavor seasoning quality <well-seasoned/bland/overly-salty>"
  ).with_additional_info(
    item_name="doneness",
    item_description="Cooking completion <undercooked/properly_cooked/overcooked>"
  ).with_additional_info(
    item_name="meat_type_accuracy",
    item_description="Correct dark/white meat received <accurate/inaccurate/partial>"
  )
)

# ORDER ACCURACY CRISIS
dct.with_topic(
  topic=Domain(
    topic="order_accuracy",
    when="Complaints about incorrect items, missing components, or wrong preparation.",
    details="Assessment of order fulfillment accuracy.",
  ).with_additional_info(
    item_name="chicken_pieces",
    item_description="Correct chicken pieces received <yes/no/partial>"
  ).with_additional_info(
    item_name="side_items",
    item_description="Accuracy of side dishes <complete/missing/incorrect>"
  ).with_additional_info(
    item_name="sauce_inclusion",
    item_description="Sauces/napkins provided <yes/no/partial>"
  )
)

# DRIVE-THRU DISASTERS
dct.with_topic(
  topic=Domain(
    topic="drive_thru",
    when="Experiences with drive-thru ordering and service.",
    details="Evaluation of drive-thru service quality.",
  ).with_additional_info(
    item_name="wait_time",
    item_description="Time spent in drive-thru <reasonable/excessive>"
  ).with_additional_info(
    item_name="order_handling",
    item_description="Handling of special requests <accommodating/inflexible>"
  ).with_additional_info(
    item_name="payment_issues",
    item_description="Problems with payment processing <none/upcharge/refusal>"
  )
)

# STAFF & MANAGEMENT
dct.with_topic(
  topic=Domain(
    topic="staff_behavior",
    when="Feedback about employee interactions or management responses.",
    details="Assessment of staff conduct and management effectiveness.",
  ).with_additional_info(
    item_name="attitude",
    item_description="Staff courtesy <polite/rude/indifferent>"
  ).with_additional_info(
    item_name="error_resolution",
    item_description="Problem resolution effectiveness <resolved/ignored/argued>"
  ).with_additional_info(
    item_name="management_presence",
    item_description="Manager involvement in issues <helpful/absent/hostile>"
  )
)

# RESTAURANT OPERATIONS
dct.with_topic(
  topic=Domain(
    topic="operations",
    when="Comments about business hours, stock availability, or facility management.",
    details="Evaluation of restaurant operational efficiency.",
  ).with_additional_info(
    item_name="closing_time_compliance",
    item_description="Adherence to posted hours <compliant/early_closure>"
  ).with_additional_info(
    item_name="stock_availability",
    item_description="Item availability during visit <fully_stocked/partial/out>"
  ).with_additional_info(
    item_name="lobby_access",
    item_description="Dining room availability <open/closed/unavailable>"
  )
)

# HEALTH & SAFETY
dct.with_topic(
  topic=Domain(
    topic="food_safety",
    when="Reports of foodborne illness or unsafe practices.",
    details="Assessment of food safety concerns.",
  ).with_additional_info(
    item_name="food_poisoning",
    item_description="Reported illness after consumption <suspected/confirmed>"
  ).with_additional_info(
    item_name="hygiene_observations",
    item_description="Observed hygiene practices <good/poor/dangerous>"
  )
)

# VALUE PROPOSITION
dct.with_topic(
  topic=Domain(
    topic="value_assessment",
    when="Comments about pricing, portion sizes, or meal deals.",
    details="Perceived value for money spent.",
  ).with_additional_info(
    item_name="portion_size",
    item_description="Serving size satisfaction <generous/skimpy/adequate>"
  ).with_additional_info(
    item_name="price_quality_ratio",
    item_description="Value perception <good/poor/neutral>"
  )
)

# DIGITAL EXPERIENCE
dct.with_topic(
  topic=Domain(
    topic="digital_orders",
    when="Mentions of online/app ordering or delivery services.",
    details="Experience with digital ordering systems.",
  ).with_additional_info(
    item_name="order_accuracy",
    item_description="Digital order correctness <accurate/incomplete/wrong>"
  ).with_additional_info(
    item_name="wait_time",
    item_description="Actual vs promised preparation time <met/exceeded>"
  )
)

# SIDE ITEMS QUALITY
dct.with_topic(
  topic=Domain(
    topic="side_dishes",
    when="Feedback on biscuits, sides, or condiments.",
    details="Quality assessment of non-chicken items.",
  ).with_additional_info(
    item_name="biscuit_quality",
    item_description="Biscuit texture and taste <fresh/stale/raw>"
  ).with_additional_info(
    item_name="side_freshness",
    item_description="Side dish quality <fresh/reheated/expired>"
  )
)

# CRISIS MANAGEMENT
dct.with_topic(
  topic=Domain(
    topic="peak_performance",
    when="Experiences during busy periods or special events.",
    details="Restaurant performance under pressure.",
  ).with_additional_info(
    item_name="staffing_level",
    item_description="Adequacy of staff during rush <sufficient/insufficient>"
  ).with_additional_info(
    item_name="stress_handling",
    item_description="Staff composure under pressure <calm/panicked/rude>"
  )
)

# COMMAND ----------

# DBTITLE 1,Advance Auto Parts
dct.with_topic(
  topic=Domain(
    topic="customer_service",
    when="Generally when the user is referring to the service they received from the staff",
    details="Summary of the review regarding the quality of service provided by the staff",
  ).with_additional_info(
    item_name="staff_friendliness",
    item_description="How friendly was the staff yes no unsure"
  ).with_additional_info(
    item_name="technical_knowledge",
    item_description="Staff knowledge and expertise in automotive parts expert average low"
  ).with_additional_info(
    item_name="service_speed",
    item_description="The speed of service fast slow average"
  )
)

dct.with_topic(
  topic=Domain(
    topic="parts_availability",
    when="When the user comments on the availability of specific auto parts they needed",
    details="Summary of the review regarding the availability of parts or items",
  ).with_additional_info(
    item_name="item_in_stock",
    item_description="Was the needed item in stock yes no unsure"
  ).with_additional_info(
    item_name="frequency_of_out_of_stock",
    item_description="Frequency of encountering out of stock items rare common always"
  )
)

dct.with_topic(
  topic=Domain(
    topic="product_quality",
    when="When the user comments on the quality or reliability of parts purchased",
    details="Summary of the review regarding the quality and reliability of parts or products",
  ).with_additional_info(
    item_name="durability",
    item_description="Durability of the purchased product high average low"
  ).with_additional_info(
    item_name="value_for_money",
    item_description="Users perception of the value for money high average low"
  )
)

dct.with_topic(
  topic=Domain(
    topic="installation_assistance",
    when="When the user discusses help received for part installation such as batteries or wipers",
    details="Summary of the review regarding installation help provided by staff",
  ).with_additional_info(
    item_name="installation_offered",
    item_description="Was installation assistance provided yes no unsure"
  ).with_additional_info(
    item_name="installation_quality",
    item_description="Quality of the installation assistance high average low"
  )
)

dct.with_topic(
  topic=Domain(
    topic="pricing_and_promotions",
    when="When the user discusses pricing discounts or promotions",
    details="Summary of the review regarding perceptions of pricing and promotions",
  ).with_additional_info(
    item_name="price_fairness",
    item_description="Perception of pricing fairness fair high low"
  ).with_additional_info(
    item_name="promotion_value",
    item_description="Value of promotions high average low"
  )
)

dct.with_topic(
  topic=Domain(
    topic="queue_management_and_wait_time",
    when="When the user comments on the efficiency of queue management or wait times",
    details="Summary of the review regarding wait times and queue handling",
  ).with_additional_info(
    item_name="wait_time",
    item_description="Time spent waiting for service short long average"
  ).with_additional_info(
    item_name="queue_management_efficiency",
    item_description="Efficiency of queue management efficient inefficient average"
  )
)

dct.with_topic(
  topic=Domain(
    topic="staff_attitude_and_behavior",
    when="When the user provides feedback on the attitude and behavior of staff members",
    details="Summary of the review regarding staff behavior",
  ).with_additional_info(
    item_name="politeness",
    item_description="Was the staff polite and courteous yes no unsure"
  ).with_additional_info(
    item_name="helpfulness",
    item_description="Was the staff helpful helpful unhelpful average"
  )
)

dct.with_topic(
  topic=Domain(
    topic="store_environment_and_cleanliness",
    when="When the user comments on store cleanliness and general environment",
    details="Summary of the review regarding store cleanliness and atmosphere",
  ).with_additional_info(
    item_name="cleanliness",
    item_description="Cleanliness of the store clean dirty average"
  ).with_additional_info(
    item_name="store_layout",
    item_description="Effectiveness of the store layout for easy navigation good poor average"
  )
)

dct.with_topic(
  topic=Domain(
    topic="return_policy_and_support",
    when="When the user discusses experiences with returning items or after sales support",
    details="Summary of the review regarding return policy and customer support",
  ).with_additional_info(
    item_name="return_policy",
    item_description="Satisfaction with the return policy satisfactory unsatisfactory unsure"
  ).with_additional_info(
    item_name="after_sales_support",
    item_description="Quality of after sales support high average low"
  )
)

dct.with_topic(
  topic=Domain(
    topic="overall_satisfaction",
    when="When the user provides general feedback on their satisfaction with the overall experience",
    details="Summary of the review regarding overall customer satisfaction",
  ).with_additional_info(
    item_name="overall_experience",
    item_description="Overall customer experience positive negative mixed"
  ).with_additional_info(
    item_name="likelihood_to_return",
    item_description="Likelihood of returning to the location high low unsure"
  )
)


# COMMAND ----------

# DBTITLE 1,Spirit Airlines
dct.with_topic(
    topic=Domain(
        topic="check_in_bag_drop",
        when="Mentions of check-in, bag drop, or kiosk usability.",
        details="Assessment of check-in and baggage drop."
    ).with_additional_info(
        item_name="self_kiosk",
        item_description="Ease of kiosk use <easy/difficult/unavailable>"
    ).with_additional_info(
        item_name="staff_assistance",
        item_description="Helpfulness of staff <helpful/unhelpful>"
    ).with_additional_info(
        item_name="bag_drop_efficiency",
        item_description="Baggage drop-off process <smooth/delayed/problematic>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="boarding",
        when="Experiences with boarding process, priority boarding, or crowd control.",
        details="Evaluation of boarding efficiency."
    ).with_additional_info(
        item_name="gate_organization",
        item_description="Clarity of announcements <clear/confusing/missing>"
    ).with_additional_info(
        item_name="timeliness",
        item_description="Punctuality of boarding <on-time/delayed/disorganized>"
    ).with_additional_info(
        item_name="staff_attitude",
        item_description="Gate staff attitude <friendly/rude/indifferent>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="in_flight_experience",
        when="Mentions of seat comfort, cleanliness, service.",
        details="Assessment of in-flight experience."
    ).with_additional_info(
        item_name="seat_comfort",
        item_description="Seat quality and legroom <comfortable/tight/unbearable>"
    ).with_additional_info(
        item_name="cleanliness",
        item_description="Cabin cleanliness <clean/dirty/filthy>"
    ).with_additional_info(
        item_name="crew_service",
        item_description="Flight attendant service <excellent/poor>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="gate_experience",
        when="Feedback on gate service, announcements, assistance.",
        details="Evaluation of gate experience."
    ).with_additional_info(
        item_name="gate_agent_attitude",
        item_description="Gate staff attitude <helpful/rude/unavailable>"
    ).with_additional_info(
        item_name="boarding_announcement",
        item_description="Clarity of instructions <clear/confusing/missing>"
    ).with_additional_info(
        item_name="delay_communication",
        item_description="Effectiveness of delay updates <transparent/misleading/no_info>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="flight_delays",
        when="Mentions of delays, cancellations, and airline handling.",
        details="Assessment of delay handling."
    ).with_additional_info(
        item_name="delay_reason_given",
        item_description="Communication of delay reasons <clear/vague/nonexistent>"
    ).with_additional_info(
        item_name="compensation_offered",
        item_description="Resolution for delays/cancellations <fair/none/unsatisfactory>"
    ).with_additional_info(
        item_name="alternative_flight",
        item_description="Rebooking experience <smooth/problematic>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="baggage_handling",
        when="Complaints about lost, damaged baggage, or claim process.",
        details="Evaluation of baggage management."
    ).with_additional_info(
        item_name="baggage_lost",
        item_description="Lost baggage <yes/no>"
    ).with_additional_info(
        item_name="damage_reported",
        item_description="Baggage condition <intact/damaged/severely_damaged>"
    ).with_additional_info(
        item_name="claim_processing",
        item_description="Ease of claim filing <easy/difficult>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="customer_service",
        when="Feedback on policies, support, and issue resolution.",
        details="Evaluation of customer service."
    ).with_additional_info(
        item_name="staff_responsiveness",
        item_description="Staff response to issues <helpful/unhelpful>"
    ).with_additional_info(
        item_name="policy_flexibility",
        item_description="Strictness of policies <reasonable/strict/unfair>"
    ).with_additional_info(
        item_name="refund_experience",
        item_description="Ease of refunds <smooth/difficult/impossible>"
    )
)

dct.with_topic(
    topic=Domain(
        topic="value_for_money",
        when="Comments on pricing, add-on fees, and perceived value.",
        details="Passenger perception of value."
    ).with_additional_info(
        item_name="ticket_price",
        item_description="Ticket pricing perception <fair/overpriced/budget-friendly>"
    ).with_additional_info(
        item_name="hidden_fees",
        item_description="Experience with extra charges <none/minor/excessive>"
    ).with_additional_info(
        item_name="overall_satisfaction",
        item_description="General value assessment <good/poor/neutral>"
    )
)

# COMMAND ----------

# DBTITLE 1,Little Caesars
# CORE FOOD QUALITY
dct.with_topic(
  topic=Domain(
    topic="pizza_quality",
    when="Mentions of pizza taste, texture, or preparation.",
    details="Evaluation of pizza preparation and taste characteristics.",
  ).with_additional_info(
    item_name="crust_texture",
    item_description="Crust consistency <crispy/soft/chewy/soggy>"
  ).with_additional_info(
    item_name="cheese_quality",
    item_description="Cheese texture and melt quality <gooey/rubbery/uneven>"
  ).with_additional_info(
    item_name="topping_distribution",
    item_description="Evenness of toppings spread <even/uneven/sparse>"
  ).with_additional_info(
    item_name="sauce_balance",
    item_description="Sauce coverage and taste <balanced/too much/too little>"
  )
)

# ORDER ACCURACY CRISIS
dct.with_topic(
  topic=Domain(
    topic="order_accuracy",
    when="Complaints about incorrect items, missing components, or wrong preparation.",
    details="Assessment of order fulfillment accuracy.",
  ).with_additional_info(
    item_name="pizza_correctness",
    item_description="Correct pizza received <yes/no/partial>"
  ).with_additional_info(
    item_name="side_items",
    item_description="Accuracy of side dishes (Crazy Bread, sauces) <complete/missing/incorrect>"
  ).with_additional_info(
    item_name="special_requests",
    item_description="Handling of customization requests <accommodated/ignored/incorrect>"
  )
)

# DRIVE-THRU & PICKUP EXPERIENCE
dct.with_topic(
  topic=Domain(
    topic="drive_thru_pickup",
    when="Experiences with drive-thru or in-store pickup ordering.",
    details="Evaluation of drive-thru and pickup service quality.",
  ).with_additional_info(
    item_name="wait_time",
    item_description="Time spent waiting <reasonable/excessive>"
  ).with_additional_info(
    item_name="order_handling",
    item_description="Handling of mobile/app orders <smooth/disorganized>"
  ).with_additional_info(
    item_name="hot_n_ready_availability",
    item_description="Availability of Hot-N-Ready pizzas <available/out of stock>"
  )
)

# STAFF & MANAGEMENT
dct.with_topic(
  topic=Domain(
    topic="staff_behavior",
    when="Feedback about employee interactions or management responses.",
    details="Assessment of staff conduct and management effectiveness.",
  ).with_additional_info(
    item_name="attitude",
    item_description="Staff courtesy <polite/rude/indifferent>"
  ).with_additional_info(
    item_name="error_resolution",
    item_description="Problem resolution effectiveness <resolved/ignored/argued>"
  ).with_additional_info(
    item_name="management_presence",
    item_description="Manager involvement in issues <helpful/absent/hostile>"
  )
)

# RESTAURANT OPERATIONS
dct.with_topic(
  topic=Domain(
    topic="operations",
    when="Comments about business hours, stock availability, or facility management.",
    details="Evaluation of restaurant operational efficiency.",
  ).with_additional_info(
    item_name="store_hours_compliance",
    item_description="Adherence to posted hours <compliant/early_closure>"
  ).with_additional_info(
    item_name="stock_availability",
    item_description="Item availability during visit <fully_stocked/partial/out>"
  ).with_additional_info(
    item_name="cleanliness",
    item_description="Restaurant cleanliness and maintenance <clean/messy/unhygienic>"
  )
)

# HEALTH & SAFETY
dct.with_topic(
  topic=Domain(
    topic="food_safety",
    when="Reports of foodborne illness or unsafe practices.",
    details="Assessment of food safety concerns.",
  ).with_additional_info(
    item_name="food_poisoning",
    item_description="Reported illness after consumption <suspected/confirmed>"
  ).with_additional_info(
    item_name="hygiene_observations",
    item_description="Observed hygiene practices <good/poor/dangerous>"
  )
)

# VALUE PROPOSITION
dct.with_topic(
  topic=Domain(
    topic="value_assessment",
    when="Comments about pricing, portion sizes, or meal deals.",
    details="Perceived value for money spent.",
  ).with_additional_info(
    item_name="portion_size",
    item_description="Serving size satisfaction <generous/skimpy/adequate>"
  ).with_additional_info(
    item_name="price_quality_ratio",
    item_description="Value perception <good/poor/neutral>"
  )
)

# DIGITAL EXPERIENCE
dct.with_topic(
  topic=Domain(
    topic="digital_orders",
    when="Mentions of online/app ordering or delivery services.",
    details="Experience with digital ordering systems.",
  ).with_additional_info(
    item_name="order_accuracy",
    item_description="Digital order correctness <accurate/incomplete/wrong>"
  ).with_additional_info(
    item_name="wait_time",
    item_description="Actual vs promised preparation time <met/exceeded>"
  )
)

# SIDE ITEMS QUALITY
dct.with_topic(
  topic=Domain(
    topic="side_dishes",
    when="Feedback on Crazy Bread, wings, or dipping sauces.",
    details="Quality assessment of non-pizza items.",
  ).with_additional_info(
    item_name="breadstick_freshness",
    item_description="Crazy Bread texture and taste <fresh/stale/raw>"
  ).with_additional_info(
    item_name="sauce_quality",
    item_description="Dipping sauce taste and freshness <flavorful/bland/spoiled>"
  )
)

# PEAK PERFORMANCE & RUSH HOUR
dct.with_topic(
  topic=Domain(
    topic="peak_performance",
    when="Experiences during busy periods or special events.",
    details="Restaurant performance under pressure.",
  ).with_additional_info(
    item_name="staffing_level",
    item_description="Adequacy of staff during rush <sufficient/insufficient>"
  ).with_additional_info(
    item_name="stress_handling",
    item_description="Staff composure under pressure <calm/panicked/rude>"
  )
)


# COMMAND ----------

dct.setup(spark)

# COMMAND ----------

spark.table(f"{dct.catalog}.{dct.schema}.{dct.table}").display()

# COMMAND ----------


