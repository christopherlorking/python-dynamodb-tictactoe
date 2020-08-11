# python-dynamodb-tictactoe

Simple CLI Tic Tac Toe game that optionaly saves game results to AWS DynamoDB via Python AWS SDK Boto3. 

> "For the things we have to learn before we can do them, we learn by doing them."
> -- <cite>Aristotle</cite>


[Amazon DynamoDB](https://aws.amazon.com/dynamodb/)

[Python AWS SDK Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

[DynamoDB free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&all-free-tier.q=dynamo&all-free-tier.q_operator=AND) (open link and scroll down...)
```sh
As of August 2020, the free tier for DynamoDB is not restricted to a 12 month period:
25 GB of storage
25 provisioned Write Capacity Units (WCU)
25 provisioned Read Capacity Units (RCU)
Enough to handle up to 200M requests per month.
```

# Requirements
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured with access/secret keys for IAM user with full DynamoDB access.
- Python 3.8.x
```sh
pip install -r requirements.txt
```

# TODO
- [x] Finish README.md
- [x] Requirements.txt
- [ ] Fetch/view previous games after game has been saved
- [ ] Create tests.py
- [ ] Containerise (add current version as a tag?)