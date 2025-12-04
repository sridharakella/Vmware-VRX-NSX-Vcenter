#--------------------------------------------------------#
#                     Spas Kaloferov                     #
#                   www.kaloferov.com                    #
# bit.ly/The-Twitter      Social     bit.ly/The-LinkedIn #
# bit.ly/The-Gitlab        Git         bit.ly/The-Github #
# bit.ly/The-BSD         License          bit.ly/The-GNU #
#--------------------------------------------------------#

  #
  #       VMware Cloud Assembly ABX Code Sample          
  #
  # [Description] 
  #   - Reads CA Secrets,  CT Encrypted Inputs, CV PG Secrets, IV PG Encrypted Constants , ABX CA Secrets and encrypted ABX Action Constants
  # [Inputs]
  #   - myEncryptedConst (Constant): ABX Action Constant
  #   - mySecret (Secret): Cloud Assembly Secret
  # [Dependency]
  # [Subscription]
  # [Blueprint]
  #   - fallowing inputs required in the cloud template: 
  #      myCtEncInput:
  #        comment: |
  #          # example of a Cloud Template Encrypted Input
  #        type: string
  #        title: My CT Enc Input
  #        encrypted: true
  #        default: my-ct-input-encrypted-value
  #        description: Cloud Template Encrypted Input
  #      myIvPgInput:
  #        comment: |
  #          # example of a Input Values Property Group
  #        type: object
  #        title: My Input Values PG
  #        $ref: /ref/property-groups/myIvPg
  #        description: Input Values Property Group
  #   - Later there are assigned as custom properties to a (machine) resource and read via the payload :
  #      properties:
  #        myCvPgSecretProp: '${propgroup.myCvPg.myPgSecret}'
  #        myIvPgEncConstProp: '${input.myIvPgInput.myPgEncConst}'
  #        mySecretProp: '${secret.mySecret}'
  #        myCtEncInputProp: '${input.myCtEncInput}'
  # [Thanks]
  #
  
def handler(context, inputs):
    
    myABXEncryptedConstIn = inputs["myEncryptedConst"]                                  # ABX Encrypted Actoins Constant
    myABXSecretIn = inputs["mySecret"]                                                  # ABX Secret 
    myPayloadCvPgSecretPropIn = inputs["customProperties"]["myCvPgSecretProp"]          # CV PG Secret 
    myPayloadIvPgEncConstPropIn = inputs["customProperties"]["myIvPgEncConstProp"]      # IV PG Encrypted Constant 
    myPayloadSecretPropIn = inputs["customProperties"]["mySecretProp"]                  # CT Secret
    myCtEncInputPropIn = inputs["customProperties"]["myCtEncInputProp"]                 # CT Encrypted Input String 
    
    print("Encrypted myABXEncryptedConst: " + myABXEncryptedConstIn)
    print("Encrypted myABXSecret: " + myABXSecretIn)
    print("Encrypted myPayloadCvPgSecretProp: " + myPayloadCvPgSecretPropIn)
    print("Encrypted myPayloadIvPgEncConstProp: " + myPayloadIvPgEncConstPropIn)
    print("Encrypted myPayloadSecretProp: " + myPayloadSecretPropIn)
    print("Encrypted myPayloadSecretProp: " + myCtEncInputPropIn)
    
    myABXEncryptedConst = context.getSecret(myABXEncryptedConstIn)
    myABXSecret = context.getSecret(myABXSecretIn)
    myPayloadCvPgSecretProp = context.getSecret(myPayloadCvPgSecretPropIn)
    myPayloadIvPgEncConstProp = context.getSecret(myPayloadIvPgEncConstPropIn)
    myPayloadSecretProp = context.getSecret(myPayloadSecretPropIn)
    myCtEncInputProp = context.getSecret(myCtEncInputPropIn)
    
    print("Decrypted myABXEncryptedConst: " + myABXEncryptedConst)
    print("Decrypted myABXSecret: " + myABXSecret)
    print("Decrypted myPayloadCvPgSecretProp: " + myPayloadCvPgSecretProp)
    print("Decrypted myPayloadIvPgEncConstProp: " + myPayloadIvPgEncConstProp)
    print("Decrypted myPayloadSecretProp: " + myPayloadSecretProp)
    print("Decrypted myPayloadSecretProp: " + myCtEncInputProp)
    
    outputs = {
      "myABXEncryptedConst": myABXEncryptedConst, 
      "myABXSecret": myABXSecret, 
      "myPayloadCvPgSecretProp": myPayloadCvPgSecretProp, 
      "myPayloadIvPgEncConstProp": myPayloadIvPgEncConstProp,
      "myPayloadSecretProp": myPayloadSecretProp, 
      "myCtEncInputProp": myCtEncInputProp
    }

    return outputs
