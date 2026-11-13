# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11011  GET              /                                                dashboard
 12573  GET              /api/abo/status                                  api_abo_status
 12554  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11701  GET              /api/automation/status                           api_automation_status
 11723  POST             /api/automation/toggle                           api_automation_toggle
 20951  GET              /api/channel/categories                          api_channel_categories
 20957  POST             /api/channel/set                                 api_channel_set
 20808  GET              /api/channels/status                             api_channels_status
 20510  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20493  GET              /api/clips                                       api_clips
 20539  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20439  GET              /api/debug/threads                               api_debug_threads
 12559  GET              /api/events                                      api_events
 12075  GET              /api/events/stream                               api_events_stream
 11938  GET              /api/health                                      api_health
 20470  POST             /api/highlights/config                           api_highlights_config
 10941  POST             /api/login                                       dashboard_login_submit
 12791  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12008  GET              /api/notify/status                               api_notify_status
 12019  POST             /api/notify/test                                 api_notify_test
 12627  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12604  GET              /api/proxy/trend                                 api_proxy_trend
 20557  GET              /api/tts/<fn>                                    api_tts_file
 21305  GET              /api/upload_window                               api_upload_window
 12177  GET              /archive/<int:eid>/download                      archive_download
 12203  GET              /download/<int:recording_id>                     download
 12136  GET              /health                                          health
 20311  GET              /healthz                                         healthz
 10932  GET              /login                                           dashboard_login_page
 10966  GET              /logout                                          dashboard_logout
 10973  GET              /manifest.webmanifest                            pwa_manifest
 21286  GET              /overlay                                         overlay_page
 10997  GET              /pwa-icon-<variant>.png                          pwa_icon
 10983  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (352)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1023  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   764  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   894  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   874  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   912  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   832  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   382  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   393  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   403  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   426  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   433  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   444  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   572  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   670  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1261  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1293  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   367  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   976  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   956  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1129  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1177  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1228  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1087  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   931  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    86  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    39  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    51  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   446  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   431  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   251  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   186  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   131  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    72  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    79  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   272  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   299  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   392  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   336  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   354  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   259  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   193  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   178  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    89  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   111  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   132  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   149  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    79  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   208  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    43  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    79  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   111  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   121  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    53  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    71  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   146  GET              /api/mcp/export                                  api_mcp_export   [nc/routes/mcp.py]
    85  GET              /api/mcp/server                                  api_mcp_server_liste   [nc/routes/mcp.py]
   111  POST             /api/mcp/server                                  api_mcp_server_anlegen   [nc/routes/mcp.py]
   116  POST             /api/mcp/server/<sid>                            api_mcp_server_aendern   [nc/routes/mcp.py]
   121  DELETE           /api/mcp/server/<sid>                            api_mcp_server_loeschen   [nc/routes/mcp.py]
   132  POST             /api/mcp/server/<sid>/test                       api_mcp_server_test   [nc/routes/mcp.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   101  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    67  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    78  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   148  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   143  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   134  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    54  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    93  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   487  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   477  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   517  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2231  /about                  Ueber diesen Bot
   968  /ai                     
  2231  /aireset                KI-Kontext zuruecksetzen
  1383  /ask                    
  1069  /assign_role            
  1119  /ban                    
  2187  /botstats               
  2231  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2231  /bulkadd                Mehrere User auf einmal tracken · a b c
  2231  /cleanup                Alte Aufnahmen aufraeumen
  1649  /clearwarns             
  2151  /clip                   
  2136  /clipoftheweek          
  1519  /clips                  
  2231  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1024  /create_category        
   995  /create_channel         
  1059  /create_group           
  1034  /create_role            
  1010  /create_voice           
  1260  /daily                  
  2231  /diag                   Vollstaendige Diagnose
  2231  /einnahmen              Einnahmen und Spenden
  1412  /event                  
  1454  /events                 
  1559  /follow                 
  1548  /help                   
  1109  /kick                   
  1232  /leaderboard            
  2231  /live                   Live-Status sofort pruefen · @user
  1506  /livenow                
  2231  /logs                   Letzte Fehler aus dem Log
  2231  /pause                  Tracking pausieren · @user
  1534  /post_test              
  1344  /profile                
  1141  /purge                  
  2231  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2231  /quota                  Speicher-Quota
  1219  /rank                   
  1494  /recstatus              
  1079  /remove_role            
  2231  /report                 Azrael-Sentinel-Wochenreport
   981  /restream_status        
  2231  /resume                 Tracking fortsetzen · @user
  1089  /set_channel_perms      
  1181  /setup_community        
  1198  /setup_targets          
  1480  /spenden                
  1591  /stats                  
   940  /status                 
  2231  /stoprec                Laufende Aufnahme sauber beenden · @user
  1687  /streaminfo             
  2231  /summary                Tageszusammenfassung
  2231  /sysres                 System-Ressourcen
  2231  /teststream             Recorder-Selbsttest · @user
  2231  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1129  /timeout                
  1659  /topstreamers           
  2231  /topusers               Top-Streamer nach Aufnahmen
   870  /track                  
  2231  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   953  /tracklist              
  1573  /unfollow               
  2231  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   902  /untrack                
  1612  /warn                   
  1635  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2398  on_member_join
  2355  on_message
  2252  on_raw_reaction_add
  2433  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (53 Funktionen)

```
  1764-1815   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  1986-2015   _clip_week_leader
  2039-2053   _clipoftheweek_loop
  2550-2612   _community_events_loop
  1721-1743   _dc_client
  1746-1755   _dc_offen
  2652-2687   _disc_automod_check
   410-415    _disc_sprache_setzen
  1818-1866   _discord_ai_automod
   673-712    _discord_automod
  1869-1889   _discord_azrael_reply
  2056-2509   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2515-2547   _ensure_error_channel
   431-444    _ensure_rank_roles
   833-847    _ensure_team_roles
  2615-2645   _error_channel_loop
   722-726    _guard
   642-670    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1934-1945   _liveboard_loop
   729-762    _on_level_up
   638-639    _par_chat_id
  2018-2036   _post_clip_of_week
  1948-1966   _post_weekly_digest
   447-473    _provision_base_channels
  1486-1580   _reg_betrieb
  1155-1249   _reg_community_setup
  1252-1333   _reg_daily_profil
  1376-1473   _reg_frage_events
   927-983    _reg_info
  1101-1152   _reg_moderation
  1336-1373   _reg_profil
  1050-1098   _reg_rollen
   986-1047   _reg_server
  1476-1483   _reg_spenden
  1583-1670   _reg_streamer
  1673-1718   _reg_system
   861-924    _reg_tracking
   797-830    _run_tg_handler
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1898-1931   _update_liveboard
  1969-1983   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (585 Funktionen, 4 Klassen)

```
 26389-26411  _abbruch_datenbank_unlesbar
  2819-2820   _abo_key
  2840-2858   _abo_probe_dump
 26511-26527  _abschied_wachen
 26530-26548  _abschluss
 16566-16573  _ad_allowlist
 17732-17738  _agent_for
 17741-17757  _ai_telemetry
 18273-18291  _alert
 22068-22118  _alert_monitor_loop
 18978-19035  _alte_beilagen_einsammeln
 22499-22561  _announce_loop
  3770-3780   _anthropic_key
  3783-3785   _anthropic_model
 10500-10503  _arg_int
  2811-2816   _as_dict
 26075-26084  _async_exc_handler
 18462-18484  _audio_tap_cmd
 19497-19556  _audio_tap_melden
 18498-18522  _audio_tap_sammler
  9849-9886   _aufnahme_beim_stopp_sichern
 18920-18941  _aufnahme_chat_ausklang
 18904-18917  _aufnahme_chat_beginnen
 19063-19084  _aufnahme_chat_dienst
 19257-19310  _aufnahme_chat_einarbeiten
 18899-18901  _aufnahme_chat_modus
 19087-19136  _aufnahme_chat_nachtrag
 18944-18975  _aufnahme_chat_vormerken
 19054-19060  _aufnahme_chat_wecken
 25200-25202  _aufnahme_deckel
 19139-19160  _aufnahme_fertigmachen
 22736-22789  _aufnahme_nach_discord
  9889-9907   _aufnahme_platz_frei
  9792-9819   _aufnahme_verteilen
 26475-26495  _aufnahmen_abschliessen
 26414-26472  _aufraeumen
 10774-10843  _auth_cookie
 10730-10770  _auth_guard
  2066-2071   _auto_on
 20182-20200  _auto_restream_loop
 14041-14083  _avatar_frames_laden
 16616-16629  _azrael_brain_kontext
 23693-23708  _azrael_broadcast_reply
 23593-23615  _azrael_chat_reply
 23565-23590  _azrael_chat_should_reply
 23621-23623  _azrael_gate_cfg
  4222-4235   _azrael_ki
 17760-17774  _azrael_live_state
  4238-4260   _azrael_lokal
 21201-21215  _azrael_overlay_state
 17816-17824  _azrael_persona_kern
 18155-18209  _azrael_proactive_loop
 17580-17636  _azrael_reaction_to_chats
 23626-23633  _azrael_reply_all_chats
  4263-4278   _azrael_schweigt_melden
 23552-23562  _azrael_self_names
 23661-23690  _azrael_send_to
 14002-14038  _azrael_spricht
 14349-14362  _azrael_stimme_stumm
 17780-17813  _azrael_system
 22202-22205  _backup_active
 22283-22296  _backup_loop
  5411-5434   _betreiber_pruefen
 25289-25293  _betrieb
 26148-26157  _brain_crowdsec_snap
 26316-26319  _brain_db_health
 21989-21998  _brain_growth_loop
 11140-11167  _brain_growth_snapshot
  2730-2764   _brain_hint_delay
 26220-26255  _brain_moderation_snap
  6684-6712   _brain_notify
 26322-26344  _brain_recording_snap
 26160-26217  _brain_restream_health
 26347-26360  _brain_tiktok_status_snap
 12054-12071  _browser_push
 14396-14400  _build_restream_cmd
  5437-5464   _can_stop_tracking
  2177-2199   _capture_set_cookies
 12657-12660  _cfg_get
 12663-12665  _cfg_set
 20912-20947  _channel_set_all
 13100-13103  _chat_connected
 13106-13122  _chat_disconnected
 19048-19051  _chat_einarbeiten_async
  9283-9313   _chat_is_forum
 18868-18893  _chat_listener_abbauen
  9455-9490   _chat_migriert
  9493-9494   _chat_migriert_async
 13136-13138  _chat_sanitize
 13085-13097  _chat_stat
  4097-4109   _check_ai_models_sync
 11408-11451  _classify_pool_anonymity
   918-940    _claude_chat_sync_metered
 10532-10538  _client_ip
 23194-23208  _clip_chat_ass
 22645-22679  _clip_prune
 22682-22692  _clip_recfile_for
 23114-23182  _clip_schneiden
 23211-23217  _clip_should_velocity
 22792-22877  _clip_to_discord
 19228-19233  _clips_abwarten
  3970-3979   _close_ai_session
 23739-23754  _cohost_broadcast
 23724-23725  _cohost_cfg
 23780-23792  _cohost_fire_highlight
 23728-23736  _cohost_gate
 23757-23777  _cohost_highlight
  7014-7075   _cookie_alarm_loop
  2267-2268   _cookie_autofetch_info
  2251-2255   _cookie_autorefresh_info
 25750-25772  _cookie_bezug_loop
 25775-25800  _cookie_bezug_runde
  2154-2158   _cookie_header
 10541-10546  _cookie_sicher
  2280-2294   _cookies_selbst_holen
  4368-4370   _create_index_safe
 21551-21665  _crowdsec_status
 21497-21548  _crowdsec_via_lapi
 21408-21426  _cscli_bin
 21435-21448  _cscli_path
  6900-6927   _daily_summary_loop
 21466-21483  _darf_journal_lesen
  3296-3321   _darf_ytdlp_nachschlagen
 12218-12239  _dashboard_adresse
 10561-10565  _dashboard_hostnamen
  1519-1549   _dashboard_trackings_umziehen
 23185-23191  _datei_weg
 22042-22065  _db_maintenance_loop
  6850-6897   _db_vacuum_loop
 16589-16613  _detect_foreign_ad
  1747-1758   _diag_path_owner
 18060-18105  _director_finalize
 19487-19494  _director_for
 18009-18057  _director_mark
 23027-23030  _disc_state_get
 23033-23040  _disc_state_set
 21970-21979  _discord_bot_starten
 21933-21944  _discord_einladung_merken
 21982-21986  _discord_invite
 21947-21967  _discord_kontext
 22988-23024  _discord_live_thread
 18212-18224  _discord_notify
 21905-21930  _discord_ops_alert
 22888-22984  _discord_post_user
 22564-22570  _discord_stop
  6930-7011   _disk_alarm_loop
 25621-25672  _disk_autoclean
 25931-25944  _disk_guard_loop
 13981-13988  _drossel_hoeher
 13977-13978  _drossel_stufe
 13991-13999  _drossel_zuruecksetzen
 12395-12397  _dump_all_threads
 25296-25310  _einstellungen_startzeile
 11335-11398  _enrich_proxies_with_geo
  2319-2380   _ensure_cookie_file_netscape
  9384-9387   _ensure_notify_topic
 11558-11595  _ensure_proxy_ready
  9323-9346   _ensure_topic
   761-763    _env_int
   766-768    _env_int_range
 18257-18270  _event_webhook
 12883-12896  _evolution_loop
  6126-6160   _extract_file_payload
 21451-21458  _f2b_sudo_hint
  1505-1516   _fanout_ziele
 26551-26614  _fatal_vom_botteil
 25205-25220  _fd_grenze_anheben
  5006-5016   _fehler_text
 11234-11252  _fetch_proxy_list
 18837-18865  _fetch_tiktok_room_id
   846-849    _ff_cmd
 19241-19254  _ffprobe_masse
 13925-13941  _fifo_schreiber_wecken
 13735-13740  _find_chromium
  3691-3693   _find_external_recorder
  2443-2445   _find_stream_urls
 12706-12731  _fire_webhooks
  7947-7957   _fork_safe
   951-964    _freeai_chat_sync_metered
  3958-3967   _get_ai_session
  7775-7815   _get_live_info
  3140-3147   _get_resolve_semaphore
  8472-8893   _handle_single_tracking
 25405-25407  _hb
 25410-25427  _hb_while
 20424-20435  _healthz_fuer_aufrufer
 25451-25479  _heap_zurueckgeben
 10847-10864  _herkunft_guard
 13150-13152  _highlight_cfg
 13155-13184  _highlight_observe
 13786-13794  _htmlov_bild_schreiben
 13764-13783  _htmlov_dauerbrowser
 13743-13761  _htmlov_screenshot_cmd
 18524-18534  _httpx_proxy
 12739-12751  _in_quiet_hours
 26375-26386  _init_db_oder_abbruch
 27228-27259  _install_fast_eventloop
 10395-10449  _install_fast_json
 12400-12416  _install_faulthandler
 20220-20229  _intel_ensure_schema
 20272-20307  _intel_index_loop
 20241-20256  _intel_index_one
 20232-20238  _intel_semantic
  5396-5409   _is_authorized
  8298-8319   _is_dead
 21486-21488  _is_private_ip
  1966-1973   _is_process_running
  6714-6721   _is_quiet_hours
  1407-1416   _is_upload_window
  4871-4886   _iso
 10549-10558  _ist_lokal
 10484-10497  _json_error_handler
  4027-4036   _ki_rueckfall_melden
  8173-8180   _kick_cluster_gefunden
  8108-8170   _kick_cluster_weiter
  6763-6805   _kick_follower_count
  6747-6750   _kick_slug
  8078-8105   _kick_ws_pause
 26363-26372  _kickmod_boot
 25716-25719  _lagebild_discord_aufnahme
 25729-25733  _lagebild_kick_chat
 25722-25726  _lagebild_overlay
 25736-25738  _lagebild_spendenziel
 25703-25713  _lagebild_upload
 12768-12770  _latest_popularity
  1903-1912   _laufstand
 25891-25928  _laufstand_loop
 25329-25367  _leistung_erheben
  7649-7676   _link_video_senden
  8459-8470   _live_check_frist_melden
  2874-2887   _live_ohne_stream
 19892-19941  _live_react_loop
 19559-19881  _live_react_worker
  3539-3653   _live_status_aufloesen
 17639-17650  _live_transcript_push
 19883-19890  _live_users
 18108-18152  _living_title_loop
 22208-22280  _local_backup_scan
  4811-4834   _lock_update
 10466-10480  _log_5xx
 25370-25402  _log_schleuse_pruefen
   836-843    _log_sicher
 14408-14420  _looks_like_codec_err
 14403-14405  _looks_like_source_expired
  7996-8026   _loop_fehler
 12419-12428  _loop_heartbeat
 25111-25144  _loop_lag_monitor
 25158-25178  _loop_stockung_melden
 25181-25191  _loop_takt_starten
 12431-12504  _loop_watchdog_thread
 17516-17533  _loyalty_add
 17507-17513  _loyalty_get
 17536-17544  _loyalty_top
  5117-5136   _manual_status
  8321-8322   _mark_dead
 11778-11794  _marketing_loop
 23640-23658  _maybe_handle_command
 26030-26054  _maybe_hype_clip
 22614-22642  _meme_klassifizieren
 19163-19225  _meme_zusammenschnitt
  4355-4360   _migrate_columns
 23922-23933  _mod_is_exempt
 23936-23941  _mod_warn_first
 23944-23947  _mod_warn_text
 12925-12944  _modlog
 12908-12922  _modlog_schreiben
  1103-1105   _multistream_targets
  3324-3360   _nachschlag_ytdlp
  7960-7961   _nc_create_subprocess_exec
  7964-7965   _nc_create_subprocess_shell
 11892-11909  _news_loop
 12967-12969  _normalize_ingest
  2661-2678   _note_check_duration
  9378-9381   _notify_topic_name
  2865-2871   _offline_ergebnis
  3363-3386   _ohne_url_melden
 17665-17673  _oracle_memories
 17960-17994  _oracle_memorize
 17676-17689  _oracle_persona
 17658-17662  _oracle_recent_text
 13359-13360  _ov_atomic_write
 13350-13352  _ov_bar
 16494-16506  _ov_clip_text
 13355-13356  _ov_oneline
 21250-21279  _overlay_push
 13689-13732  _overlay_render_size
 13036-13040  _overlay_session_reset
 21217-21219  _overlay_src_ok
 13369-13381  _overlay_takt
 16576-16586  _own_invites
 13684-13686  _parse_size
 21668-21748  _parse_ssh_attacks
  7325-7358   _pause_resume_cmd
  2205-2249   _persist_refreshed_cookies
  2108-2140   _pick_checked_pull_proxy
 10615-10630  _pin_auth_value
 10719-10720  _pin_clear_fail
 10683-10686  _pin_global_gesperrt
 10636-10647  _pin_hmac_schluessel
 10689-10696  _pin_locked
 10699-10716  _pin_note_fail
 10650-10671  _pin_ok
 21045-21070  _piper_pick_model
 21130-21195  _piper_say
 12668-12703  _post_json_threaded
 13663-13681  _probe_video_size
  1994-2011   _proc_is_recorder
 11527-11555  _proxy_pool_refresh_loop
  2074-2105   _proxy_report_recording
  9032-9113   _pruef_runde
  8991-9029   _pruefstand_melden
 25240-25251  _pruefung_verworfen
 12385-12387  _prune_stall_dumps
  2271-2277   _pull_proxy_still
 18228-18254  _push_notify
 10911-10913  _pwa_dir
 11303-11320  _quick_validate_proxy
 12734-12736  _quiet_hours_config
 10876-10909  _rate_guard
  2890-2918   _raumsperre_fragen
 17477-17483  _react_warn
  7862-7901   _reap_proc
 10568-10584  _rebinding_melden
  9722-9789   _rec_auto_abschalten
  9669-9719   _rec_frueh_getrennt
  9534-9614   _rec_kategorie_melden
  9617-9666   _rec_totstreak_fortschreiben
  2701-2723   _record_check_outcome
   831-833    _redact_stream_urls
 11454-11524  _refresh_proxy_pool
  2478-2569   _resolve_via_html
  2921-3117   _resolve_via_webcast_api_v2
  3185-3272   _resolve_via_ytdlp
 23251-23380  _resolve_youtube_ingest
  2454-2475   _resolver_stumm
 13019-13030  _restream_active_sources
 14086-14213  _restream_avatar_feeder_start
 14216-14226  _restream_avatar_feeder_stop
 19313-19451  _restream_chat_guardian
 13187-13259  _restream_chat_push
 13336-13345  _restream_chat_push_async
 26258-26313  _restream_durchreicher
 13797-13922  _restream_html_overlay_start
 13944-13964  _restream_html_overlay_stop
 12978-13001  _restream_overlay_files
 19944-19976  _restream_platform_state
 20144-20179  _restream_resume_after_restart
 13290-13307  _restream_soll_schreiben
 13310-13333  _restream_status_schreiben
 14274-14346  _restream_tts_enqueue_wav
 13625-13657  _restream_tts_feeder
 13622-13623  _restream_tts_fifo_path
 14229-14256  _restream_tts_start
 14258-14272  _restream_tts_stop
 19982-20141  _restream_verify_loop
 22173-22185  _retention_loop
 22167-22170  _retention_scan
  2822-2824   _room_is_abo
  6163-6280   _run_ai_call
 12527-12540  _run_async_from_flask
 21491-21494  _run_priv
 27217-27225  _run_selfcheck_and_exit
 22188-22199  _s3_client
  8348-8418   _safe_send
  5080-5096   _sample_net_throughput
 27197-27214  _sc_bericht
 27138-27194  _sc_dienste
 27045-27135  _sc_ki_und_stimme
 26996-27042  _sc_umgebung
  2767-2797   _schedule_next_check
 22121-22164  _scheduler_loop
  4363-4365   _schema_pk
 12543-12548  _scraper_session
 23950-23989  _screen_full
 11954-11991  _sec_headers
  2438-2440   _select_stream_from_data_section
 26906-26993  _selfcheck
  9390-9424   _send_live_notice
  1430-1434   _should_defer_upload
 22695-22733  _shrink_for_discord
 10916-10928  _sicheres_ziel
 22001-22039  _sicherheits_erinnerung_loop
 25951-25968  _sign_health_check
 25971-25990  _sign_health_loop
  4889-4914   _sitzung_bestimmen
 20407-20417  _sparen_lage
  7977-7988   _spawn
 27647-27677  _spawn_from_flask
 25254-25260  _speicher_maps
 25263-25278  _speicher_pflegen
 18536-18834  _start_chat_listener
 25223-25237  _start_gesperrt
 12507-12524  _start_loop_watchdog
 11840-11889  _stats_loop
 11819-11822  _stats_output_path
 11825-11837  _stats_write
 21082-21096  _stimme_saubern
 21103-21127  _stimme_schon_gesagt
  8972-8988   _storage_cleanup_loop
 26010-26017  _story_for
  3715-3721   _stream_url_expiry
  3723-3728   _stream_url_ttl
 16539-16546  _streamer_persona_get
 22305-22457  _system_backup
 22466-22496  _system_backup_loop
 12345-12363  _task_auf_bot_schleife
 24787-24803  _telegram_befehlsmenue
  8029-8075   _telegram_polling_fehler
  1475-1502   _telegram_ziele
 11255-11294  _test_proxy
 11750-11766  _testpush_resolve_live
 19236-19238  _text_schreiben
  9442-9452   _tg_migriert_laden
  9438-9439   _tg_migriert_pfad
  8324-8345   _tg_sprache_setzen
  9252-9262   _tg_topics_load_into_mem
  9249-9250   _tg_topics_path
  9264-9271   _tg_topics_save
 10587-10597  _token_ok
  9349-9365   _topic_anlegen
  9274-9281   _topic_forget
 12754-12765  _tracking_max_duration
  4625-4639   _tracking_remove_cleanup
  4656-4668   _tracking_resume_cleanup
  1805-1828   _try_attach_file_handler
 21072-21080  _tts_cleanup
 25675-25695  _tunnel_lage
 25836-25888  _tunnel_wacht_loop
 20575-20628  _twitch_channel_status
 23992-24140  _twitch_chat_loop
 23046-23059  _twitch_clip_versuchen
 23803-23909  _twitch_eventsub_loop
  1595-1630   _upload_queue_abarbeiten
  1453-1473   _upload_queue_add
  1566-1568   _upload_queue_count
  1436-1445   _upload_queue_load
  1633-1655   _upload_queue_nachher
  1426-1428   _upload_queue_path
  1552-1556   _upload_queue_remove
  1447-1451   _upload_queue_save
  1559-1564   _upload_queue_update
  9822-9846   _upload_rest_sichern
  1570-1592   _upload_window_loop
  7835-7842   _uptime_s
 12955-12964  _url_host
  3389-3487   _url_nachschlag
   911-915    _usage_record_claude
 26123-26145  _v37_pause_source
 26087-26097  _v37_restream_restart
 26100-26120  _v37_unpause_source
  8247-8291   _verbindung_verloren
  6808-6839   _viewer_sample_loop
 10723-10726  _wants_html
  7845-7859   _warn_empty_env
 25482-25607  _watchdog_loop
 23524-23532  _wchat_thank_ok
 25803-25833  _werkzeug_wacht_loop
 18296-18334  _whisper_get_model
  7936-7944   _whisper_native_section
 17464-17470  _whisper_pool
 18428-18460  _whisper_segments
 18336-18352  _whisper_stumm
 18355-18425  _whisper_transcribe
 13422-13579  _write_restream_overlay
 13384-13419  _write_restream_overlay_async
 24164-24263  _youtube_api_chat_loop
 20631-20734  _youtube_api_status
 20737-20804  _youtube_channel_status
 24266-24430  _youtube_chat_loop
 23062-23087  _youtube_clip_versuchen
 23386-23399  _youtube_restream_autoconfig
 23402-23426  _youtube_restream_autoconfig_inner
 23493-23521  _youtube_send
 20868-20909  _youtube_set_channel
 23429-23463  _yt_access_token
 23466-23481  _yt_live_chat_id
 23489-23490  _yt_sendrate_cfg
 24143-24158  _yt_timeout
  3164-3165   _ytdlp_detect_available
  3180-3182   _ytdlp_einzeln
  3167-3178   _ytdlp_note_result
 12390-12392  _zombie_child_count
 25313-25326  _zustand_kennzahlen
  7711-7735   about
  4544-4548   add_ai_log_entry
  4917-4988   add_recording
  4600-4617   add_tracking
  6283-6316   ai
  4118-4213   ai_chat
  4310-4320   ai_history_append
  4322-4327   ai_history_clear
  4299-4308   ai_history_load
  4284-4297   ai_rate_limit_check
  6345-6353   aireset
 17827-17846  azrael_chat
 24435-24557  brain_cmd
  3731-3736   build_recording_cmd
  4620-4623   bulk_add_trackings
  7078-7137   bulkadd
  9116-9232   check_all_trackings
  4671-4683   claim_live_transition
 16632-17396  class KickModerator
 14423-16382  class RestreamManager
  4837-4838   class _AufnahmeLockVerloren
  8183-8244   class _KickClusterSuche
 11638-11680  classify_proxy_anonymity
  6391-6590   cleanup
  5337-5343   cleanup_old_recordings
  4862-4869   clear_recording
 23090-23111  clip_moment
  7200-7276   cookies_cmd
  7279-7322   cookies_datei_cmd
  4591-4597   count_trackings_for_chat
  4531-4542   decide_preferred_recorder
  5821-5968   diag
 24669-24730  einnahmen_cmd
  4492-4508   finish_recording_attempt
  4644-4646   get_all_active_trackings
  4990-4993   get_all_recordings
  4470-4473   get_archive_entry
  2311-2316   get_cookie_health
  5060-5066   get_event_log
  4515-4529   get_last_recording_attempt
  3490-3532   get_live_status
  5071-5074   get_priority_poll_interval
  4510-4513   get_recent_recording_attempts
  4995-4998   get_recording_by_id
  3898-3927   get_redis
  5331-5335   get_storage_stats
  5110-5112   get_tiktok_status_distribution
  4685-4694   get_tracking_state
  4641-4642   get_trackings_for_group
  9910-10377  handle_recording_finished
 24779-24784  hilfe_cmd
  4378-4443   init_db
  5606-5644   live
  8421-8451   live_check_worker
  3982-4024   llm_chat
  4057-4089   llm_chat_sync
  4042-4054   llm_list_models
  5019-5052   log_event
  1928-1961   log_recording_failure
  7472-7521   logs_cmd
 26617-26896  main
  6319-6342   on_ai_media
  7598-7624   on_ai_reply
  7679-7708   on_azrael_mention
  7740-7770   on_callback
  9497-9515   on_chat_migration
  7633-7646   on_link_video
 17852-17957  oracle_handle
  7361-7364   pause_tracking
  5386-5391   profile_keyboard
  5559-5603   quelle
  7423-7469   quota
  8895-8969   reaper_loop
  5106-5108   record_tiktok_status
  6358-6388   recstatus
  3929-3937   redis_get_json
  3940-3946   redis_set_json
 24806-24816  report_cmd
 11683-11685  report_proxy_result
  2572-2614   resolve_tiktok_live_stream
  7367-7370   resume_tracking
 24819-25091  run_bot
 12242-12336  run_flask
  4551-4557   save_tiktok_check
  4841-4860   set_recording_file
  4649-4653   set_tracking_paused
 24764-24776  spenden_cmd
  9521-9532   split_and_send_video
  5469-5511   start
  4476-4490   start_recording_attempt
  6593-6631   stats
  5255-5308   stop_manual_recording
  7373-7420   stoprec
  6732-6740   summary_cmd
  7524-7595   sysres
  5970-6114   teststream
  5513-5554   tiktok
  7140-7197   topusers
  5681-5738   track
  5646-5678   track_exact
  5752-5819   tracklist
  5139-5253   trigger_manual_recording
  4773-4808   try_acquire_recording_lock
 24733-24761  unpause_cmd
  5740-5750   untrack
 24560-24666  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_zugang, sys_backup, sys_hour, sys_keep
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            aendern, class FalscheForm, get, lesen, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, bereinigen, class DateiGeaendert, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             abgelaufen, auswahl, configure, gesundheit, hat_login, kritisch, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, schnappschuesse, schnappschuesse_kappen, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, gesamtzeit, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
mcpdienste.py          class Abgelehnt, class BestandUnbekannt, class Unbekannt, export, lage, liste, llama_adresse, loeschen, speichern, testen, webui
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
oeffentlichestats.py   configure, public_stats
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            abbruch_nach, check_readonly, frist_ueberschritten, frist_unbekannt, mariadb_mit_frist, normalize, with_limit
sqlutil.py             zeitfenster_literal
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
tagesbericht.py        bauen, configure
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
