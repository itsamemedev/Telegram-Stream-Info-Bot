# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9082  GET              /                                                dashboard
 10995  GET              /api/abo/status                                  api_abo_status
 10949  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
  9870  GET              /api/automation/status                           api_automation_status
  9892  POST             /api/automation/toggle                           api_automation_toggle
 17764  GET              /api/channel/categories                          api_channel_categories
 17770  POST             /api/channel/set                                 api_channel_set
 17617  GET              /api/channels/status                             api_channels_status
 17291  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 17274  GET              /api/clips                                       api_clips
 17320  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17199  GET              /api/debug/threads                               api_debug_threads
 10960  GET              /api/events                                      api_events
 10511  GET              /api/events/stream                               api_events_stream
 10338  GET              /api/health                                      api_health
 17233  POST             /api/highlights/config                           api_highlights_config
  9016  POST             /api/login                                       dashboard_login_submit
 11285  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 10426  GET              /api/notify/status                               api_notify_status
 10437  POST             /api/notify/test                                 api_notify_test
 11049  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11026  GET              /api/proxy/trend                                 api_proxy_trend
 17340  GET              /api/tts/<fn>                                    api_tts_file
 18115  GET              /api/upload_window                               api_upload_window
 10628  GET              /archive/<int:eid>/download                      archive_download
 10656  GET              /download/<int:recording_id>                     download
 10585  GET              /health                                          health
 17168  GET              /healthz                                         healthz
  9007  GET              /login                                           dashboard_login_page
  9037  GET              /logout                                          dashboard_logout
  9044  GET              /manifest.webmanifest                            pwa_manifest
 18088  GET              /overlay                                         overlay_page
  9068  GET              /pwa-icon-<variant>.png                          pwa_icon
  9054  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (330)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   329  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   314  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   237  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   193  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   258  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   285  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   245  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
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
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   835  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   917  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   945  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   956  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   822  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   884  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   871  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   852  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   497  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   492  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   540  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   423  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   750  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   514  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   477  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   450  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   724  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   594  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   683  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   589  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   522  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   302  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   767  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   390  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   645  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   800  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   785  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   346  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   584  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   570  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   553  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   610  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1071  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1146  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1035  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   703  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   599  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   370  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   360  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   395  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
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
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (45)

```
   519  /ai                     
   992  /ask                    
   610  /assign_role            
   656  /ban                    
  1324  /botstats               
  1248  /clearwarns             
  1288  /clip                   
  1273  /clipoftheweek          
  1115  /clips                  
   571  /create_category        
   540  /create_channel         
   599  /create_group           
   582  /create_role            
   556  /create_voice           
   892  /daily                  
  1022  /event                  
  1065  /events                 
  1161  /follow                 
  1145  /help                   
   645  /kick                   
   874  /leaderboard            
  1101  /livenow                
  1131  /post_test              
   962  /profile                
   680  /purge                  
   860  /rank                   
  1088  /recstatus              
   621  /remove_role            
   533  /restream_status        
   632  /set_channel_perms      
   825  /setup_community        
   843  /setup_targets          
  1187  /stats                  
   445  /status                 
  1483  /streaminfo             
  1380  /sys_report             
  1356  /sys_unpause            
   667  /timeout                
  1259  /topstreamers           
   475  /track                  
   459  /tracklist              
  1176  /unfollow               
   508  /untrack                
  1209  /warn                   
  1233  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  1981  on_member_join
  1943  on_message
  1570  on_raw_reaction_add
  2016  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (9 Funktionen)

```
  2132-2194   _community_events_loop
  2234-2269   _disc_automod_check
   362-2091   _discord_run_once
   245-303    _discord_start
   306-359    _ensure_discord_invite
  2097-2129   _ensure_error_channel
  2197-2227   _error_channel_loop
   150-224    _uebernehmen
   227-230    starte
```

## Top-Level-Symbole in bot.py (478 Funktionen, 2 Klassen)

```
  2489-2490   _abo_key
  2510-2528   _abo_probe_dump
 14385-14392  _ad_allowlist
 15361-15367  _agent_for
 15370-15386  _ai_telemetry
 15881-15899  _alert
 18956-19006  _alert_monitor_loop
 19358-19420  _announce_loop
  3024-3027   _anthropic_key
  3034-3036   _anthropic_model
  8760-8763   _arg_int
  2481-2486   _as_dict
 16034-16056  _audio_tap_cmd
  8928-8939   _auth_cookie
  8895-8924   _auth_guard
  1755-1760   _auto_on
 17030-17048  _auto_restream_loop
 12457-12499  _avatar_frames_laden
 20420-20435  _azrael_broadcast_reply
 20320-20342  _azrael_chat_reply
 20303-20317  _azrael_chat_should_reply
 20348-20350  _azrael_gate_cfg
 15391-15405  _azrael_live_state
 18001-18015  _azrael_overlay_state
 15763-15817  _azrael_proactive_loop
 15209-15265  _azrael_reaction_to_chats
 20353-20360  _azrael_reply_all_chats
 20290-20300  _azrael_self_names
 20388-20417  _azrael_send_to
 12418-12454  _azrael_spricht
 15411-15432  _azrael_system
 19090-19093  _backup_active
 19171-19184  _backup_loop
 18895-18904  _brain_growth_loop
  9261-9288   _brain_growth_snapshot
  2423-2443   _brain_hint_delay
  5785-5813   _brain_notify
 10490-10507  _browser_push
  5825-5912   _build_daily_summary
 12717-12721  _build_restream_cmd
  4607-4634   _can_stop_tracking
  1868-1890   _capture_set_cookies
 11103-11106  _cfg_get
 11109-11111  _cfg_set
 17725-17760  _channel_set_all
 11654-11657  _chat_connected
 11660-11676  _chat_disconnected
  7902-7913   _chat_is_forum
 16362-16387  _chat_listener_abbauen
 11696-11698  _chat_sanitize
 11639-11651  _chat_stat
 11679-11682  _chat_stats_snapshot
  3307-3319   _check_ai_models_sync
  9543-9586   _classify_pool_anonymity
  9589-9606   _classify_pool_anonymity_bg
   837-859    _claude_chat_sync_metered
  8789-8796   _client_ip
 19504-19531  _clip_prune
 19534-19544  _clip_recfile_for
 19954-19960  _clip_should_velocity
 19585-19667  _clip_to_discord
  3200-3209   _close_ai_session
 20466-20481  _cohost_broadcast
 20451-20452  _cohost_cfg
 20507-20519  _cohost_fire_highlight
 20455-20463  _cohost_gate
 20484-20504  _cohost_highlight
  9191-9193   _conv_messages
  6184-6245   _cookie_alarm_loop
  1959-1964   _cookie_autofetch_info
  1942-1946   _cookie_autorefresh_info
  1845-1849   _cookie_header
  1976-2009   _cookies_selbst_holen
  3513-3525   _create_index_safe
 18447-18553  _crowdsec_status
 18393-18444  _crowdsec_via_lapi
 18297-18315  _cscli_bin
 18324-18337  _cscli_path
  6074-6099   _daily_summary_loop
 18355-18372  _darf_journal_lesen
 18930-18953  _db_maintenance_loop
  6043-6071   _db_vacuum_loop
 14408-14432  _detect_foreign_ad
  1490-1501   _diag_path_owner
 15669-15713  _director_finalize
 16545-16552  _director_for
 15618-15666  _director_mark
 19819-19822  _disc_state_get
 19825-19832  _disc_state_set
 18876-18885  _discord_bot_starten
 18840-18851  _discord_einladung_merken
 18888-18892  _discord_invite
 18854-18873  _discord_kontext
 19780-19816  _discord_live_thread
 15820-15832  _discord_notify
 18812-18837  _discord_ops_alert
 19678-19776  _discord_post_user
 19423-19429  _discord_stop
  6102-6179   _disk_alarm_loop
 21896-21945  _disk_autoclean
 21948-21961  _disk_guard_loop
 12396-12403  _drossel_hoeher
 12392-12393  _drossel_stufe
 12406-12414  _drossel_zuruecksetzen
 10781-10783  _dump_all_threads
  9469-9532   _enrich_proxies_with_geo
  2038-2099   _ensure_cookie_file_netscape
  7961-7964   _ensure_notify_topic
  9713-9750   _ensure_proxy_ready
  7915-7942   _ensure_topic
   696-698    _env_int
   701-703    _env_int_range
 15865-15878  _event_webhook
 11454-11467  _evolution_loop
  5227-5261   _extract_file_payload
  2171-2173   _extract_urls_from_streamurl_node
 18340-18347  _f2b_sudo_hint
  4107-4117   _fehler_text
  9370-9388   _fetch_proxy_list
 16331-16359  _fetch_tiktok_room_id
   769-772    _ff_cmd
 12233-12238  _find_chromium
  2955-2957   _find_external_recorder
  2176-2178   _find_stream_urls
 11154-11179  _fire_webhooks
  7011-7020   _fork_safe
   870-883    _freeai_chat_sync_metered
 18386-18390  _geo_lookup_ips
  3188-3197   _get_ai_session
  6844-6884   _get_live_info
  2707-2714   _get_resolve_semaphore
  7244-7616   _handle_single_tracking
 21718-21720  _hb
 21723-21740  _hb_while
 11710-11712  _highlight_cfg
 11715-11744  _highlight_observe
 12241-12259  _htmlov_screenshot_cmd
 16058-16068  _httpx_proxy
 11187-11199  _in_quiet_hours
 22812-22843  _install_fast_eventloop
  8655-8709   _install_fast_json
 10786-10802  _install_faulthandler
 17076-17085  _intel_ensure_schema
 17123-17158  _intel_index_loop
 17097-17107  _intel_index_one
 17088-17094  _intel_semantic
  4596-4605   _is_authorized
  7145-7151   _is_dead
  2161-2163   _is_hevc
 18375-18377  _is_private_ip
  1654-1661   _is_process_running
  5815-5822   _is_quiet_hours
  1283-1292   _is_upload_window
  3972-3987   _iso
  8744-8757   _json_error_handler
  6037-6038   _kick_broadcaster_id
  5949-5991   _kick_follower_count
  5933-5936   _kick_slug
 10303-10310  _kick_user_token
  3562-3565   _kind_from_filename
 11216-11218  _latest_popularity
 16766-16799  _live_react_loop
 16556-16755  _live_react_worker
 15268-15279  _live_transcript_push
 16757-16764  _live_users
 15716-15760  _living_title_loop
 19096-19168  _local_backup_scan
  8726-8740   _log_5xx
 12729-12741  _looks_like_codec_err
 12724-12726  _looks_like_source_expired
  7061-7091   _loop_fehler
 10806-10815  _loop_heartbeat
 21688-21715  _loop_lag_monitor
 10818-10886  _loop_watchdog_thread
 15148-15162  _loyalty_add
 15139-15145  _loyalty_get
 15165-15173  _loyalty_top
 11326-11328  _manual_donations_total
  4314-4333   _manual_status
  7153-7154   _mark_dead
  9989-10005  _marketing_loop
 20367-20385  _maybe_handle_command
 22047-22071  _maybe_hype_clip
 19473-19501  _meme_klassifizieren
  3480-3503   _migrate_columns
 20646-20657  _mod_is_exempt
 20660-20665  _mod_warn_first
 20668-20671  _mod_warn_text
 11494-11502  _modlog
  1011-1013   _multistream_targets
  7023-7024   _nc_create_subprocess_exec
  7027-7028   _nc_create_subprocess_shell
 10240-10257  _news_loop
 11521-11523  _normalize_ingest
  2354-2371   _note_check_duration
  7955-7958   _notify_topic_name
 15294-15302  _oracle_memories
 15567-15601  _oracle_memorize
 15305-15318  _oracle_persona
 15287-15291  _oracle_recent_text
 11867-11868  _ov_atomic_write
 11858-11860  _ov_bar
 14311-14323  _ov_clip_text
 11863-11864  _ov_oneline
 18052-18081  _overlay_push
 12187-12230  _overlay_render_size
 11590-11594  _overlay_session_reset
 18017-18019  _overlay_src_ok
 14395-14405  _own_invites
 12182-12184  _parse_size
 18561-18641  _parse_ssh_attacks
  6446-6479   _pause_resume_cmd
  1896-1940   _persist_refreshed_cookies
  1799-1831   _pick_checked_pull_proxy
  8825-8838   _pin_auth_value
  8884-8885   _pin_clear_fail
  8864-8867   _pin_locked
  8870-8881   _pin_note_fail
  8841-8861   _pin_ok
 17861-17886  _piper_pick_model
 17946-17995  _piper_say
 11116-11151  _post_json_threaded
 12161-12179  _probe_video_size
  1682-1699   _proc_is_recorder
  9682-9710   _proxy_pool_refresh_loop
  1765-1796   _proxy_report_recording
 10771-10773  _prune_stall_dumps
 10059-10180  _public_stats
  1967-1973   _pull_proxy_still
 15836-15862  _push_notify
  8986-8988   _pwa_dir
  9439-9454   _quick_validate_proxy
 11182-11184  _quiet_hours_config
  8951-8984   _rate_guard
 15109-15115  _react_warn
  6931-6970   _reap_proc
  2394-2416   _record_check_outcome
   764-766    _redact_stream_urls
  9609-9679   _refresh_proxy_pool
  2187-2277   _resolve_via_html
  2530-2684   _resolve_via_webcast_api_v2
  2747-2809   _resolve_via_ytdlp
 19994-20123  _resolve_youtube_ingest
 11573-11584  _restream_active_sources
 12502-12565  _restream_avatar_feeder_start
 12568-12577  _restream_avatar_feeder_stop
 16390-16509  _restream_chat_guardian
 11747-11819  _restream_chat_push
 11844-11853  _restream_chat_push_async
 12262-12363  _restream_html_overlay_start
 12366-12379  _restream_html_overlay_stop
 11532-11555  _restream_overlay_files
 16803-16835  _restream_platform_state
 16992-17027  _restream_resume_after_restart
 12625-12683  _restream_tts_enqueue_wav
 12123-12155  _restream_tts_feeder
 12120-12121  _restream_tts_fifo_path
 12580-12607  _restream_tts_start
 12609-12623  _restream_tts_stop
 16841-16989  _restream_verify_loop
 19061-19073  _retention_loop
 19055-19058  _retention_scan
  2492-2494   _room_is_abo
  5265-5382   _run_ai_call
 10909-10922  _run_async_from_flask
 18380-18383  _run_priv
 22800-22808  _run_selfcheck_and_exit
 19076-19087  _s3_client
  7180-7231   _safe_send
  4240-4256   _sample_net_throughput
  2446-2467   _schedule_next_check
 19009-19052  _scheduler_loop
  3506-3510   _schema_pk
 10926-10931  _scraper_session
 20674-20713  _screen_full
 10354-10391  _sec_headers
  2166-2168   _select_stream_from_data_section
 22588-22797  _selfcheck
  7967-8001   _send_live_notice
  1306-1310   _should_defer_upload
 19547-19582  _shrink_for_discord
  8991-9003   _sicheres_ziel
 18907-18927  _sicherheits_erinnerung_loop
 21968-21985  _sign_health_check
 21988-22007  _sign_health_loop
  3990-4015   _sitzung_bestimmen
  7040-7051   _spawn
 23218-23248  _spawn_from_flask
 16070-16328  _start_chat_listener
 10889-10906  _start_loop_watchdog
 10207-10235  _stats_loop
 10186-10189  _stats_output_path
 10192-10204  _stats_write
 17898-17912  _stimme_saubern
 17919-17943  _stimme_schon_gesagt
  7695-7711   _storage_cleanup_loop
 22027-22034  _story_for
  2980-2986   _stream_url_expiry
  2988-2993   _stream_url_ttl
 14358-14365  _streamer_persona_get
 19193-19315  _system_backup
 19324-19354  _system_backup_loop
 10731-10749  _task_auf_bot_schleife
  9391-9430   _test_proxy
  9937-9953   _testpush_resolve_live
  7156-7177   _tg_sprache_setzen
  7874-7884   _tg_topics_load_into_mem
  7871-7872   _tg_topics_path
  7886-7893   _tg_topics_save
  8799-8807   _token_ok
  7896-7900   _topic_forget
 11202-11213  _tracking_max_duration
  3770-3784   _tracking_remove_cleanup
  3801-3813   _tracking_resume_cleanup
  1548-1571   _try_attach_file_handler
 17888-17896  _tts_cleanup
  9913-9917   _tunnel_effective
 17384-17437  _twitch_channel_status
 20716-20861  _twitch_chat_loop
 19838-19851  _twitch_clip_versuchen
 20530-20633  _twitch_eventsub_loop
  1329-1342   _upload_queue_add
  1353-1355   _upload_queue_count
  1312-1321   _upload_queue_load
  1302-1304   _upload_queue_path
  1344-1351   _upload_queue_remove
  1323-1327   _upload_queue_save
  1357-1398   _upload_window_loop
  6904-6911   _uptime_s
 11509-11518  _url_host
   830-834    _usage_record_claude
  7094-7138   _verbindung_verloren
  5994-6025   _viewer_sample_loop
  8888-8891   _wants_html
  6914-6928   _warn_empty_env
 21761-21882  _watchdog_loop
 20269-20277  _wchat_thank_ok
 15904-15934  _whisper_get_model
  7001-7008   _whisper_native_section
 15096-15102  _whisper_pool
 16003-16032  _whisper_segments
 15936-16000  _whisper_transcribe
 11915-12077  _write_restream_overlay
 11877-11912  _write_restream_overlay_async
 20885-20965  _youtube_api_chat_loop
 17440-17543  _youtube_api_status
 17546-17613  _youtube_channel_status
 20968-21129  _youtube_chat_loop
 19854-19879  _youtube_clip_versuchen
 20129-20142  _youtube_restream_autoconfig
 20145-20169  _youtube_restream_autoconfig_inner
 20236-20264  _youtube_send
 17681-17722  _youtube_set_channel
 20172-20206  _yt_access_token
 20209-20224  _yt_live_chat_id
 20232-20233  _yt_sendrate_cfg
 20864-20879  _yt_timeout
  2731-2732   _ytdlp_detect_available
  2734-2745   _ytdlp_note_result
 10776-10778  _zombie_child_count
  6780-6804   about
  3681-3685   add_ai_log_entry
  3598-3601   add_archive_entry
  4278-4280   add_archive_rule
  4018-4089   add_recording
  3745-3762   add_tracking
  5385-5418   ai
  3333-3384   ai_chat
  3418-3428   ai_history_append
  3430-3435   ai_history_clear
  3407-3416   ai_history_load
  3392-3405   ai_rate_limit_check
  5447-5455   aireset
 15435-15454  azrael_chat
 21134-21256  brain_cmd
  2996-3001   build_recording_cmd
  3765-3768   bulk_add_trackings
  6248-6307   bulkadd
  7714-7854   check_all_trackings
  3817-3829   claim_live_transition
 14435-15028  class KickModerator
 12744-14198  class RestreamManager
  9796-9838   classify_proxy_anonymity
  5493-5691   cleanup
  4532-4538   cleanup_old_recordings
  3963-3970   clear_recording
 19882-19951  clip_moment
  4230-4233   compute_storage_forecast
  6370-6443   cookies_cmd
  3736-3742   count_trackings_for_chat
  3668-3679   decide_preferred_recorder
  3608-3611   delete_archive_entry
  4282-4284   delete_archive_rule
  4922-5069   diag
 21368-21429  einnahmen_cmd
  4224-4227   find_recordings_by_fingerprint
  3629-3645   finish_recording_attempt
  3789-3791   get_all_active_trackings
  3696-3698   get_all_checks
  4091-4094   get_all_recordings
  4173-4175   get_all_tags_with_counts
  4201-4204   get_annotations_for_recording
  3603-3606   get_archive_entry
  4194-4197   get_bookmarked_recordings
  2026-2031   get_cookie_health
  4161-4167   get_event_log
  3652-3666   get_last_recording_attempt
  2812-2917   get_live_status
  4471-4474   get_manual_recordings
  4209-4212   get_or_compute_inspect_sync
  4573-4576   get_outcome_breakdown
  4180-4183   get_priority_poll_interval
  3647-3650   get_recent_recording_attempts
  4096-4099   get_recording_by_id
  4187-4190   get_recording_note
  3134-3157   get_redis
  3725-3728   get_stats
  4526-4530   get_storage_stats
  4302-4304   get_tiktok_status_distribution
  3831-3840   get_tracking_state
  3786-3787   get_trackings_for_group
  4487-4490   get_trash_recordings
  8019-8634   handle_recording_finished
  3528-3553   init_db
  4274-4276   list_archive_rules
  4726-4764   live
  7234-7242   live_check_worker
  3212-3246   llm_chat
  3269-3297   llm_chat_sync
  3254-3266   llm_list_models
  4120-4153   log_event
  1616-1649   log_recording_failure
  6593-6642   logs_cmd
 22075-22578  main
  5421-5444   on_ai_media
  6719-6745   on_ai_reply
  6748-6777   on_azrael_mention
  6809-6839   on_callback
 15460-15564  oracle_handle
  6482-6485   pause_tracking
  4586-4591   profile_keyboard
  6544-6590   quota
  7618-7692   reaper_loop
  4298-4300   record_tiktok_status
  5460-5490   recstatus
  3159-3167   redis_get_json
  3170-3176   redis_set_json
 21432-21442  report_cmd
  9841-9843   report_proxy_result
  2280-2307   resolve_tiktok_live_stream
  4482-4485   restore_recording
  6488-6491   resume_tracking
  4287-4292   run_archive_rules
 21445-21668  run_bot
 10670-10722  run_flask
  4262-4265   sample_bandwidth_for_active
  3688-3694   save_tiktok_check
  3955-3961   set_recording_file
  3794-3798   set_tracking_paused
  4477-4480   soft_delete_recording
  8007-8017   split_and_send_video
  4639-4681   start
  3613-3627   start_recording_attempt
  5694-5732   stats
  4452-4469   stop_manual_recording
  6494-6541   stoprec
  5918-5926   summary_cmd
  6645-6716   sysres
  5071-5215   teststream
  4683-4724   tiktok
  6310-6367   topusers
  4801-4858   track
  4766-4798   track_exact
  4872-4920   tracklist
  4336-4450   trigger_manual_recording
  3916-3953   try_acquire_recording_lock
  4493-4495   universal_search
  4860-4870   untrack
 21259-21365  update_cmd
  4219-4222   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      avatar_kette, drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livefolge.py           live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_bitrate, drossel_overlay_aus, drossel_preset
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
