#--------------------------------------------------------#
#                     Spas Kaloferov                     #
#                   www.kaloferov.com                    #
# bit.ly/The-Twitter      Social     bit.ly/The-LinkedIn #
# bit.ly/The-Gitlab        Git        bit.ly/The-Youtube #
# bit.ly/The-BSD         License          bit.ly/The-GNU #
#--------------------------------------------------------#

  #
  #       VMware Cloud Assembly ABX Code Sample          
  #
  # [Description] 
  #   - Changes the IP Address of a machine resource
  # [Inputs]
  # [Dependency]
    # [Subscription]
  #   - Event Topics:
  #      - network.configure (BLOCKING)
  # [Blueprint]
  # [Thanks]
  #

# ----- Global ----- #  


# ----- Functions  ----- # 

def handler(context, inputs):   # Action entry function.

    fn = " handler - "    # Funciton name 
    print("[ABX]"+fn+"Action started.")
    print("[ABX]"+fn+"Function started.")

    # ----- Inputs  ----- #  
    
    # Create array for the addresses
    # addresses = [[]]
    
    # New IP Address to assign
    newIPAddress = str('172.16.20.56')
    
    # ----- Outputs ----- #
    
    outputs = {}
    # outputs["addresses"] = addresses
    # outputs["addresses"][0] = newIPAddress
    outputs = {
        "addresses" : [[newIPAddress]]
    }
    
    print("[ABX]"+fn+"Function completed.")   
    
    return outputs    # Function Return 
    # End Function   
